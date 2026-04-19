from unittest.mock import AsyncMock, MagicMock, patch
from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from app.crew.tools.fact_check_search import FactCheckSearchTool
from app.services.fact_check_service import (
	_normalize_fact_check_output,
	_run_fact_check,
	_resolve_fact_check_orchestrator,
	_run_fact_check_with_langgraph,
	_run_fact_check_with_retry,
	_validate_fact_check_payload,
	check_claim,
)


def _fact_check_payload(verdict: str = "FALSE", confidence_score: float = 0.92) -> dict:
	return {
		"verdict": verdict,
		"explanation": "Multiple sources confirm this verdict.",
		"confidence_score": confidence_score,
		"sources": [{"title": "Fact Check", "url": "http://factcheck.com", "snippet": "..."}],
	}


@pytest.fixture
async def auth_headers(client) -> dict:
	register_payload = {
		"email": "fact-check-user@example.com",
		"password": "password123",
		"display_name": "Fact Check User",
	}
	await client.post("/auth/register", json=register_payload)
	login_resp = await client.post(
		"/auth/login",
		json={"email": register_payload["email"], "password": register_payload["password"]},
	)
	token = login_resp.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_fact_check_crew():
	mock_kickoff = AsyncMock(return_value=MagicMock(raw=_fact_check_payload()))
	mock_crew = MagicMock(kickoff_async=mock_kickoff)
	with patch("app.services.fact_check_service.CrewFactory.create_fact_check_crew", return_value=mock_crew):
		yield mock_kickoff


def test_fact_check_search_tool_name_matches_enum():
	tool = FactCheckSearchTool()
	assert tool.name == "fact_check_search"


async def test_fact_check_search_tool_arun_returns_list():
	with patch("app.crew.tools.fact_check_search.AsyncTavilyClient") as mock_tavily:
		mock_instance = AsyncMock()
		mock_tavily.return_value = mock_instance
		mock_instance.search.return_value = {
			"results": [
				{"title": "Check", "url": "http://factcheck.com", "content": "The claim is false"}
			]
		}
		tool = FactCheckSearchTool()
		result = await tool._arun(claim="The earth is flat")
		assert isinstance(result, list)


@pytest.mark.asyncio
async def test_post_fact_check_returns_verdict(client, mock_fact_check_crew):
	response = await client.post("/fact-check", json={"claim": "The earth is flat"})
	assert response.status_code == 200
	data = response.json()
	assert data["verdict"] in ("TRUE", "FALSE", "UNVERIFIED")
	assert 0.0 <= data["confidence_score"] <= 1.0


@pytest.mark.asyncio
async def test_fact_check_logged_with_null_user_id_when_anonymous(client, mock_fact_check_crew, db):
	await client.post("/fact-check", json={"claim": "Anonymous claim"})
	result = await db.execute(text("SELECT user_id FROM fact_checks ORDER BY created_at DESC LIMIT 1"))
	user_id = result.scalar()
	assert user_id is None


@pytest.mark.asyncio
async def test_fact_check_logged_with_user_id_when_authenticated(client, auth_headers, mock_fact_check_crew, db):
	await client.post("/fact-check", json={"claim": "Auth claim"}, headers=auth_headers)
	result = await db.execute(text("SELECT user_id FROM fact_checks ORDER BY created_at DESC LIMIT 1"))
	user_id = result.scalar()
	assert user_id is not None


@pytest.mark.asyncio
async def test_fact_check_history_requires_auth(client):
	response = await client.get("/fact-check/history")
	assert response.status_code == 401


@pytest.mark.asyncio
async def test_fact_check_history_returns_user_checks(client, auth_headers, mock_fact_check_crew):
	mock_fact_check_crew.return_value = MagicMock(raw=_fact_check_payload(verdict="TRUE", confidence_score=0.5))
	await client.post("/fact-check", json={"claim": "Claim 1"}, headers=auth_headers)
	await client.post("/fact-check", json={"claim": "Claim 2"}, headers=auth_headers)

	response = await client.get("/fact-check/history", headers=auth_headers)
	assert response.status_code == 200
	assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_false_claim_returns_false_verdict(client, mock_fact_check_crew):
	mock_fact_check_crew.return_value = MagicMock(raw=_fact_check_payload(verdict="FALSE", confidence_score=0.95))
	response = await client.post("/fact-check", json={"claim": "Known false claim"})
	assert response.json()["verdict"] == "FALSE"


@pytest.mark.asyncio
async def test_get_fact_check_by_id_returns_single_record(client, auth_headers, mock_fact_check_crew):
	post_response = await client.post("/fact-check", json={"claim": "Single record"}, headers=auth_headers)
	fact_check_id = post_response.json()["id"]

	get_response = await client.get(f"/fact-check/{fact_check_id}", headers=auth_headers)
	assert get_response.status_code == 200
	assert get_response.json()["id"] == fact_check_id


@pytest.mark.asyncio
async def test_get_fact_check_by_id_requires_auth(client, mock_fact_check_crew):
	post_response = await client.post("/fact-check", json={"claim": "No auth read"})
	fact_check_id = post_response.json()["id"]

	response = await client.get(f"/fact-check/{fact_check_id}")
	assert response.status_code == 401


@pytest.mark.asyncio
async def test_post_fact_check_empty_claim_returns_422(client):
	response = await client.post("/fact-check", json={"claim": ""})
	assert response.status_code == 422


@pytest.mark.asyncio
async def test_check_claim_confidence_score_out_of_range_raises_db_error(db, monkeypatch):
	async def fake_fact_result(_claim: str) -> dict:
		return {
			"verdict": "UNVERIFIED",
			"explanation": "Out-of-range confidence for constraint test.",
			"confidence_score": 1.5,
			"sources": [],
		}

	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_retry", fake_fact_result)

	with pytest.raises(IntegrityError):
		await check_claim("Constraint claim", None, db)

	await db.rollback()


@pytest.mark.asyncio
async def test_orchestrator_env_disabled_forces_crewai(monkeypatch):
	monkeypatch.setattr("app.services.fact_check_service.settings.ENABLE_LANGGRAPH", False)
	mock_db = AsyncMock()
	mock_db.get.return_value = SimpleNamespace(orchestrator="langgraph")

	orchestrator = await _resolve_fact_check_orchestrator(user_id=object(), db=mock_db)
	assert orchestrator == "crewai"


@pytest.mark.asyncio
async def test_orchestrator_env_enabled_uses_user_preference(monkeypatch):
	monkeypatch.setattr("app.services.fact_check_service.settings.ENABLE_LANGGRAPH", True)
	mock_db = AsyncMock()
	mock_db.get.return_value = SimpleNamespace(orchestrator="langgraph")

	orchestrator = await _resolve_fact_check_orchestrator(user_id=object(), db=mock_db)
	assert orchestrator == "langgraph"


def test_validate_fact_check_payload_rejects_invalid_confidence():
	with pytest.raises(Exception):
		_validate_fact_check_payload(
			{
				"verdict": "TRUE",
				"explanation": "Invalid confidence should fail validation.",
				"confidence_score": 1.5,
				"sources": [],
			}
		)


def test_validate_fact_check_payload_coerces_string_sources_to_dicts():
	payload = _validate_fact_check_payload(
		{
			"verdict": "FALSE",
			"explanation": "Checked against multiple public sources.",
			"confidence_score": 0.77,
			"sources": [
				"https://en.wikipedia.org/wiki/Muharrem_%C4%B0nce",
				"short text source",
			],
		}
	)

	assert payload["sources"][0]["url"].startswith("https://")
	assert payload["sources"][1]["snippet"] == "short text source"


@pytest.mark.asyncio
async def test_run_fact_check_with_retry_retries_on_empty_llm_response(monkeypatch):
	mock_crew = MagicMock()
	mock_crew.kickoff_async = AsyncMock(
		side_effect=[
			Exception("Invalid response from LLM call - None or empty."),
			MagicMock(raw=_fact_check_payload(verdict="TRUE", confidence_score=0.85)),
		]
	)

	monkeypatch.setattr(
		"app.services.fact_check_service.CrewFactory.create_fact_check_crew",
		lambda *args, **kwargs: mock_crew,
	)
	monkeypatch.setattr("app.services.fact_check_service.asyncio.sleep", AsyncMock(return_value=None))

	result = await _run_fact_check_with_retry("retry claim")

	assert result["verdict"] == "TRUE"
	assert mock_crew.kickoff_async.await_count == 2


@pytest.mark.asyncio
async def test_run_fact_check_returns_unverified_on_known_upstream_error(monkeypatch):
	async def fail_with_empty_response(_claim: str) -> dict:
		raise Exception("Invalid response from LLM call - None or empty.")

	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_retry", fail_with_empty_response)

	result = await _run_fact_check(claim="any claim", orchestrator="crewai")

	assert result["verdict"] == "UNVERIFIED"
	assert result["confidence_score"] == 0.2


@pytest.mark.asyncio
async def test_langgraph_runner_passes_configured_recursion_limit(monkeypatch):
	captured_config = {}

	class FakeGraph:
		async def ainvoke(self, _state, config=None):
			captured_config.update(config or {})
			return {
				"verdict_payload": {
					"verdict": "UNVERIFIED",
					"explanation": "No conclusive sources.",
					"confidence_score": 0.33,
					"sources": [],
				}
			}

	monkeypatch.setattr("app.services.fact_check_service._build_fact_check_graph", lambda: FakeGraph())
	monkeypatch.setattr("app.services.fact_check_service.settings.LANGGRAPH_RECURSION_LIMIT", 17)

	result = await _run_fact_check_with_langgraph("test claim")

	assert captured_config["recursion_limit"] == 17
	assert result["verdict"] == "UNVERIFIED"


def test_normalize_fact_check_output_parses_markdown_wrapped_json():
	raw = """```json
{"verdict": "FALSE", "explanation": "Checked", "confidence_score": 0.7, "sources": []}
```"""

	parsed = _normalize_fact_check_output(raw)
	assert parsed["verdict"] == "FALSE"
	assert parsed["confidence_score"] == 0.7


@pytest.mark.asyncio
async def test_langgraph_runner_raises_when_payload_missing(monkeypatch):
	class EmptyGraph:
		async def ainvoke(self, _state, config=None):
			return {}

	monkeypatch.setattr("app.services.fact_check_service._build_fact_check_graph", lambda: EmptyGraph())

	with pytest.raises(ValueError):
		await _run_fact_check_with_langgraph("test claim")


@pytest.mark.asyncio
async def test_post_fact_check_uses_langgraph_when_enabled_and_user_prefers_it(client, auth_headers, monkeypatch):
	monkeypatch.setattr("app.services.fact_check_service.settings.ENABLE_LANGGRAPH", True)

	langgraph_payload = {
		"verdict": "TRUE",
		"explanation": "LangGraph path was selected.",
		"confidence_score": 0.81,
		"sources": [{"title": "Source", "url": "http://langgraph.test", "snippet": "..."}],
	}

	async def fake_langgraph(_claim: str) -> dict:
		return langgraph_payload

	async def fake_crewai(_claim: str) -> dict:  # pragma: no cover - should not be called
		raise AssertionError("CrewAI path should not run when user preference is langgraph and env is enabled")

	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_langgraph", fake_langgraph)
	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_retry", fake_crewai)

	pref_response = await client.patch(
		"/users/me/preferences",
		json={"orchestrator": "langgraph"},
		headers=auth_headers,
	)
	assert pref_response.status_code == 200

	response = await client.post(
		"/fact-check",
		json={"claim": "Test claim for langgraph selection"},
		headers=auth_headers,
	)

	assert response.status_code == 200
	assert response.json()["verdict"] == "TRUE"
	assert response.json()["explanation"] == "LangGraph path was selected."


@pytest.mark.asyncio
async def test_post_fact_check_env_override_false_forces_crewai_even_if_user_prefers_langgraph(client, auth_headers, monkeypatch):
	monkeypatch.setattr("app.services.fact_check_service.settings.ENABLE_LANGGRAPH", False)

	crewai_payload = {
		"verdict": "FALSE",
		"explanation": "CrewAI path was forced by env override.",
		"confidence_score": 0.76,
		"sources": [{"title": "Source", "url": "http://crewai.test", "snippet": "..."}],
	}

	async def fake_langgraph(_claim: str) -> dict:  # pragma: no cover - should not be called
		raise AssertionError("LangGraph path should not run when ENABLE_LANGGRAPH is false")

	async def fake_crewai(_claim: str) -> dict:
		return crewai_payload

	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_langgraph", fake_langgraph)
	monkeypatch.setattr("app.services.fact_check_service._run_fact_check_with_retry", fake_crewai)

	pref_response = await client.patch(
		"/users/me/preferences",
		json={"orchestrator": "langgraph"},
		headers=auth_headers,
	)
	assert pref_response.status_code == 200

	response = await client.post(
		"/fact-check",
		json={"claim": "Test claim for env override forcing crewai"},
		headers=auth_headers,
	)

	assert response.status_code == 200
	assert response.json()["verdict"] == "FALSE"
	assert response.json()["explanation"] == "CrewAI path was forced by env override."
