from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from app.crew.tools.fact_check_search import FactCheckSearchTool
from app.services.fact_check_service import check_claim


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
