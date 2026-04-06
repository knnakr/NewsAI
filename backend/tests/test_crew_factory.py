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
