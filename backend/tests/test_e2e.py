import pytest
from sqlalchemy import text

from app.crew.hooks import on_tool_used
from app.middleware import rate_limiter


@pytest.fixture
async def auth_headers(client) -> dict[str, str]:
	await client.post(
		"/auth/register",
		json={
			"email": "security-user@example.com",
			"password": "password123",
			"display_name": "Security User",
		},
	)
	login_response = await client.post(
		"/auth/login",
		json={
			"email": "security-user@example.com",
			"password": "password123",
		},
	)
	token = login_response.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def clear_rate_limit_state():
	"""Keep auth-rate-limit state isolated per test function."""
	rate_limiter._request_counts.clear()
	yield
	rate_limiter._request_counts.clear()


async def test_rate_limit_returns_429_after_threshold(client):
	for _ in range(11):
		await client.post("/auth/login", json={"email": "rate@test.com", "password": "wrong"})

	response = await client.post("/auth/login", json={"email": "rate@test.com", "password": "wrong"})
	assert response.status_code == 429


async def test_rate_limit_does_not_affect_non_auth_endpoints(client):
	for _ in range(15):
		response = await client.get("/health")

	assert response.status_code == 200


async def test_hashed_password_not_in_user_response(client, auth_headers):
	response = await client.get("/users/me", headers=auth_headers)

	assert "hashed_password" not in response.json()
	assert "hashed_password" not in str(response.json())


async def test_token_hash_not_in_any_response(client, auth_headers):
	response = await client.get("/users/me", headers=auth_headers)

	assert "token_hash" not in str(response.json())


async def test_cors_disallows_unknown_origins(client):
	response = await client.get("/health", headers={"Origin": "https://evil-site.com"})

	assert response.headers.get("access-control-allow-origin") != "https://evil-site.com"


async def test_sql_injection_attempt_returns_safe_response(client, auth_headers):
	response = await client.get("/news/feed?category=' OR '1'='1", headers=auth_headers)

	assert response.status_code in (200, 422)
	assert "error" not in str(response.json()).lower() or response.status_code == 422


@pytest.mark.asyncio
async def test_e2e_scenario_1_full_chat_flow_news_crew(client, auth_headers, db, monkeypatch):
	async def fake_run_news_crew_with_tool_logging(**kwargs):
		await on_tool_used(
			source=None,
			event=type(
				"ToolEvent",
				(),
				{
					"tool_name": "web_search",
					"tool_input": {"query": "latest ai news"},
					"tool_output": [{"url": "https://example.com/news"}],
					"duration_ms": 12,
					"error": None,
				},
			)(),
		)
		return "AI answer with source https://example.com/news"

	monkeypatch.setattr(
		"app.services.crew_service._run_news_crew_with_retry",
		fake_run_news_crew_with_tool_logging,
	)

	create_conversation_response = await client.post("/conversations", headers=auth_headers)
	assert create_conversation_response.status_code == 201
	conversation_id = create_conversation_response.json()["id"]

	first_message_response = await client.post(
		f"/conversations/{conversation_id}/messages",
		json={"content": "Latest AI news today?"},
		headers=auth_headers,
	)
	assert first_message_response.status_code == 200
	assert first_message_response.json()["role"] == "assistant"

	tool_call_count_result = await db.execute(
		text("SELECT COUNT(*) FROM agent_tool_calls WHERE tool_name = 'web_search'")
	)
	assert (tool_call_count_result.scalar() or 0) >= 1

	follow_up_response = await client.post(
		f"/conversations/{conversation_id}/messages",
		json={"content": "Can you summarize this in 3 bullets?"},
		headers=auth_headers,
	)
	assert follow_up_response.status_code == 200

	conversation_response = await client.get(f"/conversations/{conversation_id}", headers=auth_headers)
	assert conversation_response.status_code == 200
	assert len(conversation_response.json()["messages"]) >= 4

	archive_response = await client.post(f"/conversations/{conversation_id}/archive", headers=auth_headers)
	assert archive_response.status_code == 200
	archive_db_result = await db.execute(
		text(f"SELECT is_archived FROM conversations WHERE id = '{conversation_id}'")
	)
	assert archive_db_result.scalar() is True


@pytest.mark.asyncio
async def test_e2e_scenario_2_fact_check_anonymous_then_authenticated(client, auth_headers, db, monkeypatch):
	fake_fact_result = {
		"verdict": "UNVERIFIED",
		"explanation": "Not enough independent evidence.",
		"confidence_score": 0.41,
		"sources": [{"title": "Source", "url": "https://example.com", "snippet": "..."}],
	}

	async def fake_fact_check_retry(claim: str):
		return fake_fact_result

	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_retry", fake_fact_check_retry)

	anon_response = await client.post("/fact-check", json={"claim": "Anonymous claim"})
	assert anon_response.status_code == 200

	anon_db_result = await db.execute(
		text("SELECT user_id FROM fact_checks WHERE claim = 'Anonymous claim' ORDER BY created_at DESC LIMIT 1")
	)
	assert anon_db_result.scalar() is None

	auth_response = await client.post(
		"/fact-check",
		json={"claim": "Authenticated claim"},
		headers=auth_headers,
	)
	assert auth_response.status_code == 200

	auth_db_result = await db.execute(
		text("SELECT user_id FROM fact_checks WHERE claim = 'Authenticated claim' ORDER BY created_at DESC LIMIT 1")
	)
	assert auth_db_result.scalar() is not None


@pytest.mark.asyncio
async def test_e2e_scenario_3_article_cache_flow(client, db, monkeypatch):
	call_count = {"count": 0}

	async def fake_get_or_fetch_articles(category: str, from_date: str | None = None):
		call_count["count"] += 1
		return [
			{
				"title": f"Article {call_count['count']}",
				"url": f"https://example.com/{call_count['count']}",
				"source_name": "MockSource",
				"published_at": None,
				"ai_summary": None,
				"category": category,
			}
		]

	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)

	first_response = await client.get("/news/feed?category=technology")
	assert first_response.status_code == 200
	assert call_count["count"] == 1

	second_response = await client.get("/news/feed?category=technology")
	assert second_response.status_code == 200
	assert call_count["count"] == 1

	await db.execute(
		text(
			"UPDATE article_cache SET expires_at = NOW() - INTERVAL '1 hour' "
			"WHERE cache_key = 'technology:default'"
		)
	)
	await db.commit()

	third_response = await client.get("/news/feed?category=technology")
	assert third_response.status_code == 200
	assert call_count["count"] == 2


@pytest.mark.asyncio
async def test_e2e_scenario_4_auth_security_flow(client, db):
	await client.post(
		"/auth/register",
		json={
			"email": "auth-flow@example.com",
			"password": "password123",
			"display_name": "Auth Flow",
		},
	)

	for _ in range(5):
		wrong_login_response = await client.post(
			"/auth/login",
			json={"email": "auth-flow@example.com", "password": "wrong-password"},
		)
		assert wrong_login_response.status_code == 401

	locked_response = await client.post(
		"/auth/login",
		json={"email": "auth-flow@example.com", "password": "password123"},
	)
	assert locked_response.status_code == 423

	await db.execute(
		text(
			"UPDATE users SET locked_until = NOW() - INTERVAL '16 minutes', failed_login_count = 0 "
			"WHERE email = 'auth-flow@example.com'"
		)
	)
	await db.commit()

	unlocked_login_response = await client.post(
		"/auth/login",
		json={"email": "auth-flow@example.com", "password": "password123"},
	)
	assert unlocked_login_response.status_code == 200
	old_refresh = unlocked_login_response.cookies.get("refresh_token")
	assert old_refresh

	client.cookies.set("refresh_token", old_refresh)
	refresh_response = await client.post("/auth/refresh")
	assert refresh_response.status_code == 200

	client.cookies.set("refresh_token", old_refresh)
	old_refresh_again_response = await client.post("/auth/refresh")
	assert old_refresh_again_response.status_code == 401
