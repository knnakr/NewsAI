"""Tests for CrewAI setup and tool initialization (Tasks 3.4 and 3.5)."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.crew.hooks import on_tool_used
from app.crew.agents.news_fetcher import create_groq_llm, create_news_fetcher_agent
from app.crew.agents.news_analyst import create_news_analyst_agent
from app.crew.news_crew import build_news_crew, run_news_crew
from app.crew.tasks.news_tasks import create_analysis_task, create_fetch_task
from app.crew.tools.summarize import SummarizeArticleTool
from app.crew.utils import _context_stack, clear_tool_call_context, set_tool_call_context
from app.crew.tools.web_search import WebSearchTool
from app.models.conversation import AgentToolCall, Conversation, Message
from app.models.user import User
from app.schemas.conversation import MessageCreate
from app.services.crew_service import run_chat_crew


@pytest.fixture
async def auth_headers(client) -> dict:
	register_payload = {
		"email": "crew-user1@example.com",
		"password": "password123",
		"display_name": "Crew User 1",
	}
	await client.post("/auth/register", json=register_payload)
	login_resp = await client.post(
		"/auth/login",
		json={"email": register_payload["email"], "password": register_payload["password"]},
	)
	token = login_resp.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def auth_headers_user2(client) -> dict:
	register_payload = {
		"email": "crew-user2@example.com",
		"password": "password123",
		"display_name": "Crew User 2",
	}
	await client.post("/auth/register", json=register_payload)
	login_resp = await client.post(
		"/auth/login",
		json={"email": register_payload["email"], "password": register_payload["password"]},
	)
	token = login_resp.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_crew_service():
	mock_run = AsyncMock(return_value=("Assistant response with source https://example.com/src", [{"url": "https://example.com/src"}]))
	with patch("app.routers.conversations.run_chat_crew", new=mock_run):
		yield mock_run


@pytest.fixture
def mock_stream_crew_service():
	async def _run_chat_crew(*args, **kwargs):
		step_callback = kwargs.get("step_callback")
		if step_callback:
			step_callback(SimpleNamespace(result="Search result draft"))
			step_callback(SimpleNamespace(output="Assistant response with source https://example.com/src", text="Assistant response with source https://example.com/src"))
		return ("Assistant response with source https://example.com/src", [{"url": "https://example.com/src"}])

	mock_run = AsyncMock(side_effect=_run_chat_crew)
	with patch("app.routers.conversations.run_chat_crew", new=mock_run):
		yield mock_run


def test_create_news_fetcher_agent_returns_agent():
	with patch("app.crew.agents.news_fetcher.LLM"):
		agent = create_news_fetcher_agent(MagicMock())
		assert agent is not None
		assert agent.role == "News Fetcher"


def test_news_fetcher_agent_has_web_search_tool():
	with patch("app.crew.agents.news_fetcher.LLM"):
		agent = create_news_fetcher_agent(MagicMock())
		tool_names = [t.name for t in agent.tools]
		assert "web_search" in tool_names


def test_news_fetcher_agent_has_max_iter_set():
	with patch("app.crew.agents.news_fetcher.LLM"):
		agent = create_news_fetcher_agent(MagicMock())
		assert agent.max_iter == 5


def test_max_iter_prevents_infinite_loop():
	with patch("app.crew.news_crew.LLM"):
		crew = build_news_crew()
		fetcher_agent = crew.agents[0]
		assert fetcher_agent.max_iter == 5


def test_create_groq_llm_handles_rate_limit_error():
	with patch("app.crew.agents.news_fetcher.LLM", side_effect=Exception("RateLimitError: too many requests")):
		with pytest.raises(RuntimeError, match="RateLimitError"):
			create_groq_llm()


def test_create_groq_llm_handles_api_connection_error():
	with patch("app.crew.agents.news_fetcher.LLM", side_effect=Exception("APIConnectionError: network unavailable")):
		with pytest.raises(RuntimeError, match="APIConnectionError"):
			create_groq_llm()


def test_web_search_tool_name_matches_enum():
	tool = WebSearchTool()
	assert tool.name == "web_search"


def test_web_search_tool_has_description():
	tool = WebSearchTool()
	assert len(tool.description) > 0


async def test_web_search_tool_arun_returns_list():
	with patch("app.crew.tools.web_search.AsyncTavilyClient") as mock_tavily:
		mock_instance = AsyncMock()
		mock_tavily.return_value = mock_instance
		mock_instance.search.return_value = {
			"results": [{"title": "Test", "url": "http://test.com", "content": "Test content"}],
		}
		tool = WebSearchTool()
		result = await tool._arun(query="test news")
		assert isinstance(result, list)
		assert len(result) == 1
		assert "title" in result[0]
		assert "url" in result[0]


async def test_web_search_tool_returns_empty_on_no_results():
	with patch("app.crew.tools.web_search.AsyncTavilyClient") as mock_tavily:
		mock_instance = AsyncMock()
		mock_tavily.return_value = mock_instance
		mock_instance.search.return_value = {"results": []}
		tool = WebSearchTool()
		result = await tool._arun(query="obscure query")
		assert result == []


def test_summarize_tool_name_matches_enum():
	tool = SummarizeArticleTool()
	assert tool.name == "summarize_article"


async def test_summarize_tool_arun_returns_string():
	with patch("app.crew.tools.summarize.httpx.AsyncClient") as mock_client:
		mock_response = MagicMock()
		mock_response.text = "<html><body>Article content here</body></html>"
		mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
		tool = SummarizeArticleTool()
		result = await tool._arun(url="http://test.com/article")
		assert isinstance(result, str)


async def test_summarize_tool_handles_fetch_error():
	with patch("app.crew.tools.summarize.httpx.AsyncClient") as mock_client:
		mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("fetch error"))
		tool = SummarizeArticleTool()
		result = await tool._arun(url="http://invalid.com")
		assert "hata" in result.lower() or result == ""


def test_news_analyst_agent_goal_includes_language():
	agent = create_news_analyst_agent(MagicMock(), "English", "formal")
	assert "English" in agent.goal


def test_news_analyst_agent_goal_includes_tone():
	agent = create_news_analyst_agent(MagicMock(), "Turkish", "casual")
	assert "casual" in agent.goal


def test_news_analyst_agent_has_summarize_tool():
	agent = create_news_analyst_agent(MagicMock(), "Turkish", "neutral")
	tool_names = [tool.name for tool in agent.tools]
	assert "summarize_article" in tool_names


def test_news_fetcher_agent_backstory_mentions_tavily():
	agent = create_news_fetcher_agent(MagicMock())
	assert "Tavily" in agent.backstory or len(agent.backstory) > 0


def test_fetch_task_description_includes_user_message():
	agent = create_news_fetcher_agent(MagicMock())
	task = create_fetch_task(agent, "Tech news today", [])
	assert "Tech news today" in task.description


def test_fetch_task_includes_conversation_history():
	agent = create_news_fetcher_agent(MagicMock())
	history = [{"role": "user", "content": "previous question"}]
	task = create_fetch_task(agent, "follow up", history)
	assert "previous question" in task.description


def test_fetch_task_limits_history_to_10_messages():
	agent = create_news_fetcher_agent(MagicMock())
	history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
	task = create_fetch_task(agent, "new question", history)
	assert "msg 0" not in task.description
	assert "msg 19" in task.description


def test_analysis_task_uses_fetch_task_as_context():
	agent = create_news_analyst_agent(MagicMock(), "Turkish", "neutral")
	fetch_task = create_fetch_task(create_news_fetcher_agent(MagicMock()), "initial question", [])
	analysis_task = create_analysis_task(agent, fetch_task)
	assert fetch_task in analysis_task.context


def test_build_news_crew_returns_crew_with_2_agents():
	with patch("app.crew.news_crew.LLM"):
		crew = build_news_crew()
		assert len(crew.agents) == 2


@pytest.mark.asyncio
async def test_run_news_crew_returns_result_raw():
	with patch("app.crew.news_crew.LLM"):
		with patch("app.crew.news_crew.Crew") as mock_crew_class:
			mock_crew = MagicMock()
			mock_crew.agents = [
				create_news_fetcher_agent(MagicMock()),
				create_news_analyst_agent(MagicMock(), "Turkish", "neutral"),
			]
			mock_crew.kickoff_async = AsyncMock(return_value=MagicMock(raw="crew raw output"))
			mock_crew_class.return_value = mock_crew

			result = await run_news_crew(
				user_message="latest tech news",
				conversation_history=[],
				language="Turkish",
				ai_tone="neutral",
			)

			assert result == "crew raw output"


def test_set_tool_call_context_stores_message_id():
	import uuid

	message_id = uuid.uuid4()
	set_tool_call_context(message_id, MagicMock(), uuid.uuid4())
	assert _context_stack["message_id"] == message_id


def test_clear_tool_call_context_empties_stack():
	set_tool_call_context(MagicMock(), MagicMock(), MagicMock())
	clear_tool_call_context()
	assert _context_stack == {}


@pytest.mark.asyncio
async def test_tool_call_logged_to_agent_tool_calls_table(db):
	user = User(email="crew-log@example.com", display_name="Crew Log User")
	db.add(user)
	await db.flush()

	conversation = Conversation(user_id=user.id, title="Tool log test")
	db.add(conversation)
	await db.flush()

	message = Message(conversation_id=conversation.id, role="assistant", content="assistant message")
	db.add(message)
	await db.commit()

	set_tool_call_context(message.id, db, user.id)
	event = MagicMock()
	event.tool_name = "web_search"
	event.tool_input = {"query": "latest tech news"}
	event.tool_output = "search output"
	event.duration_ms = 120
	event.error = None

	await on_tool_used(None, event)
	clear_tool_call_context()

	result = await db.execute(select(AgentToolCall).where(AgentToolCall.message_id == message.id))
	call = result.scalar_one_or_none()
	assert call is not None
	assert call.tool_name == "web_search"
	assert call.is_success is True


@pytest.mark.asyncio
async def test_tool_call_failure_logged_with_is_success_false(db):
	user = User(email="crew-fail@example.com", display_name="Crew Fail User")
	db.add(user)
	await db.flush()

	conversation = Conversation(user_id=user.id, title="Tool fail log test")
	db.add(conversation)
	await db.flush()

	message = Message(conversation_id=conversation.id, role="assistant", content="assistant message")
	db.add(message)
	await db.commit()

	set_tool_call_context(message.id, db, user.id)
	event = MagicMock()
	event.tool_name = "web_search"
	event.tool_input = {"query": "claim verification"}
	event.tool_output = ""
	event.duration_ms = 50
	event.error = "tool failure"

	await on_tool_used(None, event)
	clear_tool_call_context()

	result = await db.execute(select(AgentToolCall).where(AgentToolCall.message_id == message.id))
	call = result.scalar_one_or_none()
	assert call is not None
	assert call.is_success is False
	assert call.error_message == "tool failure"


@pytest.mark.asyncio
async def test_run_chat_crew_returns_string_and_sources():
	with patch("app.services.crew_service.run_news_crew", new=AsyncMock(return_value="Tech recap: https://example.com/a")):
		result, sources = await run_chat_crew(
			user_message="Tech news?",
			conversation_history=[],
			user_preferences={"language": "Turkish", "ai_tone": "neutral"},
			db=MagicMock(),
			message_id=uuid.uuid4(),
		)

		assert isinstance(result, str)
		assert isinstance(sources, list)


@pytest.mark.asyncio
async def test_run_chat_crew_uses_language_from_preferences():
	mock_run_news_crew = AsyncMock(return_value="News summary")
	with patch("app.services.crew_service.run_news_crew", new=mock_run_news_crew):
		await run_chat_crew(
			user_message="News?",
			conversation_history=[],
			user_preferences={"language": "English", "ai_tone": "formal"},
			db=MagicMock(),
			message_id=uuid.uuid4(),
		)

		mock_run_news_crew.assert_awaited_once_with(
			"News?",
			[],
			"English",
			"formal",
			step_callback=None,
		)


def test_message_create_rejects_empty_content():
	with pytest.raises(ValidationError):
		MessageCreate(content="")


def test_message_create_rejects_too_long_content():
	with pytest.raises(ValidationError):
		MessageCreate(content="x" * 4001)


def test_message_create_valid():
	msg = MessageCreate(content="What is the latest tech news?")
	assert msg.content == "What is the latest tech news?"


@pytest.mark.asyncio
async def test_post_conversations_creates_conversation(client, auth_headers):
	response = await client.post("/conversations", headers=auth_headers)
	assert response.status_code == 201
	assert "id" in response.json()


@pytest.mark.asyncio
async def test_get_conversations_returns_only_current_user(client, auth_headers, auth_headers_user2):
	await client.post("/conversations", headers=auth_headers)
	await client.post("/conversations", headers=auth_headers)
	await client.post("/conversations", headers=auth_headers_user2)

	response = await client.get("/conversations", headers=auth_headers)
	assert response.status_code == 200
	assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_access_other_user_conversation_returns_403(client, auth_headers, auth_headers_user2):
	create_resp = await client.post("/conversations", headers=auth_headers_user2)
	conv_id = create_resp.json()["id"]

	response = await client.get(f"/conversations/{conv_id}", headers=auth_headers)
	assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_conversation_soft_deletes(client, auth_headers):
	create_resp = await client.post("/conversations", headers=auth_headers)
	conv_id = create_resp.json()["id"]

	delete_response = await client.delete(f"/conversations/{conv_id}", headers=auth_headers)
	assert delete_response.status_code == 200

	response = await client.get(f"/conversations/{conv_id}", headers=auth_headers)
	assert response.status_code == 404


@pytest.mark.asyncio
async def test_send_message_creates_user_and_assistant_messages(client, auth_headers, mock_crew_service):
	create_resp = await client.post("/conversations", headers=auth_headers)
	conv_id = create_resp.json()["id"]

	response = await client.post(
		f"/conversations/{conv_id}/messages",
		json={"content": "What is trending in tech?"},
		headers=auth_headers,
	)

	assert response.status_code == 200
	assert response.json()["role"] == "assistant"


@pytest.mark.asyncio
async def test_conversation_history_included_in_crew_call(client, auth_headers, mock_crew_service):
	create_resp = await client.post("/conversations", headers=auth_headers)
	conv_id = create_resp.json()["id"]

	await client.post(
		f"/conversations/{conv_id}/messages",
		json={"content": "First question"},
		headers=auth_headers,
	)
	await client.post(
		f"/conversations/{conv_id}/messages",
		json={"content": "Follow up"},
		headers=auth_headers,
	)

	call_args = mock_crew_service.call_args
	assert len(call_args.kwargs["conversation_history"]) >= 2


@pytest.mark.asyncio
async def test_send_message_stream_returns_sse_and_persists_assistant_message(client, auth_headers, mock_stream_crew_service, db):
	create_resp = await client.post("/conversations", headers=auth_headers)
	conv_id = create_resp.json()["id"]

	async with client.stream(
		"POST",
		f"/conversations/{conv_id}/messages/stream",
		json={"content": "What is trending in tech?"},
		headers=auth_headers,
	) as response:
		assert response.status_code == 200
		body = await response.aread()

	stream_text = body.decode()
	assert '"event": "token"' in stream_text
	assert '[DONE]' in stream_text
	assert mock_stream_crew_service.await_count == 1

	result = await db.execute(
		select(Message).where(Message.conversation_id == uuid.UUID(conv_id)).order_by(Message.created_at.asc())
	)
	messages = list(result.scalars().all())
	assert len(messages) >= 2
	assert messages[-1].role == "assistant"
	assert messages[-1].content == "Assistant response with source https://example.com/src"
