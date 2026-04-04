from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import text

from app.config import settings
from app.crew.agents.fact_checker import create_fact_checker_agent
from app.crew.agents.verdict_agent import create_verdict_agent
from app.crew.tasks.fact_check_tasks import create_research_task, create_verdict_task
from app.crew.tools.fact_check_search import FactCheckSearchTool


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


def test_fact_checker_agent_has_both_tools():
	agent = create_fact_checker_agent(MagicMock())
	tool_names = [tool.name for tool in agent.tools]
	assert "fact_check_search" in tool_names
	assert "web_search" in tool_names


def test_fact_checker_agent_has_max_iter():
	agent = create_fact_checker_agent(MagicMock())
	assert agent.max_iter == 5


def test_verdict_agent_has_no_tools():
	agent = create_verdict_agent(MagicMock())
	assert len(agent.tools) == 0


def test_verdict_agent_uses_reasoning_model():
	with patch("app.crew.agents.verdict_agent.LLM") as mock_llm:
		create_verdict_agent(MagicMock())
		call_args = mock_llm.call_args
		assert settings.GROQ_MODEL_REASONING in str(call_args)


def test_research_task_description_includes_claim():
	agent = MagicMock()
	with patch("app.crew.tasks.fact_check_tasks.Task") as mock_task:
		create_research_task(agent, "The earth is flat")
		description = mock_task.call_args.kwargs["description"]
		assert "The earth is flat" in description


def test_research_task_asks_for_multiple_sources():
	agent = MagicMock()
	with patch("app.crew.tasks.fact_check_tasks.Task") as mock_task:
		create_research_task(agent, "test claim")
		description = mock_task.call_args.kwargs["description"]
		assert "3" in description or "multiple" in description.lower() or "farkli" in description.lower()


def test_verdict_task_uses_research_task_as_context():
	agent = MagicMock()
	research_task = MagicMock()
	with patch("app.crew.tasks.fact_check_tasks.Task") as mock_task:
		create_verdict_task(agent, research_task)
		context = mock_task.call_args.kwargs["context"]
		assert research_task in context


def test_verdict_task_expected_output_is_json():
	agent = MagicMock()
	with patch("app.crew.tasks.fact_check_tasks.Task") as mock_task:
		create_verdict_task(agent, MagicMock())
		expected_output = mock_task.call_args.kwargs["expected_output"]
		assert "JSON" in expected_output or "json" in expected_output


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
	mock_run = AsyncMock(
		return_value={
			"verdict": "FALSE",
			"explanation": "Multiple sources confirm this is false.",
			"confidence_score": 0.92,
			"sources": [{"title": "Fact Check", "url": "http://factcheck.com", "snippet": "..."}],
		}
	)
	with patch("app.services.fact_check_service.run_fact_check_crew", new=mock_run):
		yield mock_run


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
	mock_fact_check_crew.return_value = {
		"verdict": "TRUE",
		"explanation": "t",
		"confidence_score": 0.5,
		"sources": [],
	}
	await client.post("/fact-check", json={"claim": "Claim 1"}, headers=auth_headers)
	await client.post("/fact-check", json={"claim": "Claim 2"}, headers=auth_headers)

	response = await client.get("/fact-check/history", headers=auth_headers)
	assert response.status_code == 200
	assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_false_claim_returns_false_verdict(client, mock_fact_check_crew):
	mock_fact_check_crew.return_value = {
		"verdict": "FALSE",
		"explanation": "False claim.",
		"confidence_score": 0.95,
		"sources": [],
	}
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
