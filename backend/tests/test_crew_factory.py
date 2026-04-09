from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.crew.crew_factory import CrewFactory


@pytest.mark.asyncio
async def test_create_news_crew_returns_news_crew_instance():
	crew = CrewFactory.create_news_crew(
		user_message="latest tech news",
		conversation_history=[],
		language="Turkish",
		ai_tone="neutral",
	)
	assert crew is not None
	assert len(crew.agents) == 2
	assert len(crew.tasks) == 2


@pytest.mark.asyncio
async def test_create_fact_check_crew_returns_fact_check_crew_instance():
	crew = CrewFactory.create_fact_check_crew(claim="A test claim")
	assert crew is not None
	assert len(crew.agents) == 2
	assert len(crew.tasks) == 2


@pytest.mark.asyncio
async def test_news_crew_kickoff_raw_is_returned_from_service():
	with patch("app.services.crew_service.CrewFactory.create_news_crew") as mock_factory:
		mock_crew = SimpleNamespace(kickoff_async=AsyncMock(return_value=SimpleNamespace(raw="news output")))
		mock_factory.return_value = mock_crew

		from app.services.crew_service import _run_news_crew_with_retry

		result = await _run_news_crew_with_retry(
			user_message="msg",
			conversation_history=[],
			language="Turkish",
			ai_tone="neutral",
			step_callback=None,
		)

		assert result == "news output"


@pytest.mark.asyncio
async def test_run_article_summary_crew_retries_provider_role_error():
	with patch("app.services.crew_service.CrewFactory.create_news_summary_crew") as mock_factory:
		first_crew = SimpleNamespace(
			kickoff_async=AsyncMock(side_effect=Exception("OpenAIException - last message role must be 'user'"))
		)
		second_crew = SimpleNamespace(kickoff_async=AsyncMock(return_value=SimpleNamespace(raw="Final summary")))
		mock_factory.side_effect = [first_crew, second_crew]

		from app.services.crew_service import run_article_summary_crew

		result = await run_article_summary_crew(
			article_url="https://example.com/a",
			article_title="Sample",
			article_source="Example",
			article_category="technology",
		)

		assert result == "Final summary"
		assert mock_factory.call_count == 2


@pytest.mark.asyncio
async def test_run_article_summary_crew_raises_non_retryable_error():
	with patch("app.services.crew_service.CrewFactory.create_news_summary_crew") as mock_factory:
		failing_crew = SimpleNamespace(kickoff_async=AsyncMock(side_effect=Exception("provider crashed hard")))
		mock_factory.return_value = failing_crew

		from app.services.crew_service import run_article_summary_crew

		with pytest.raises(Exception, match="provider crashed hard"):
			await run_article_summary_crew(
				article_url="https://example.com/a",
				article_title="Sample",
				article_source="Example",
				article_category="technology",
			)

		assert mock_factory.call_count == 1
