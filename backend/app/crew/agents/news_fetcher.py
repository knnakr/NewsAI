"""News Fetcher agent factory and Groq LLM setup (Task 3.4)."""

from __future__ import annotations

import logging

from crewai import Agent, LLM

from app.config import settings
from app.crew.llm_config import crewai_model_kwargs
from app.crew.tools.fetch_news import FetchNewsTool
from app.crew.tools.fetch_trending import FetchTrendingTool
from app.crew.tools.web_search import WebSearchTool

logger = logging.getLogger(__name__)


def create_groq_llm() -> LLM:
	"""Create a Groq-backed CrewAI LLM with Task 3.4 defaults."""
	try:
		return LLM(
			api_key=settings.GROQ_API_KEY,
			**crewai_model_kwargs(settings.GROQ_MODEL_DEFAULT),
			temperature=0.3,
		)
	except Exception as exc:  # pragma: no cover - exact exception classes vary by provider SDK
		error_text = f"{type(exc).__name__}: {exc}"
		if "RateLimitError" in error_text:
			logger.warning("Groq RateLimitError while creating LLM: %s", exc)
			raise RuntimeError("RateLimitError: Groq API rate limit reached") from exc
		if "APIConnectionError" in error_text:
			logger.warning("Groq APIConnectionError while creating LLM: %s", exc)
			raise RuntimeError("APIConnectionError: Could not connect to Groq API") from exc
		raise


try:
	groq_llm = create_groq_llm()
except RuntimeError:
	# Keep import safe; runtime call sites can decide how to react.
	groq_llm = None


def create_news_fetcher_agent(llm: LLM | None) -> Agent:
	"""Build News Fetcher agent with web search capability."""
	active_llm = llm or create_groq_llm()
	return Agent(
		role="News Fetcher",
		goal="Kullanıcının sorusuyla ilgili güncel ve güvenilir haberleri bul.",
		backstory=(
			"Sen deneyimli bir araştırmacısın. "
			"Tavily arama motoru ile en güncel haberleri bulur, "
			"kaynaklarını belgelersin."
		),
		tools=[WebSearchTool(), FetchNewsTool(), FetchTrendingTool()],
		llm=active_llm,
		verbose=True,
		max_iter=5,
	)
