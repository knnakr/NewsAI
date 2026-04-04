from __future__ import annotations

from collections.abc import Callable

from crewai import Crew, LLM, Process

from app.config import settings
from app.crew.agents.news_analyst import create_news_analyst_agent
from app.crew.agents.news_fetcher import create_news_fetcher_agent
from app.crew.llm_config import crewai_model_kwargs
from app.crew.tasks.news_tasks import create_analysis_task, create_fetch_task


def build_news_crew(language: str = "Turkish", ai_tone: str = "neutral", step_callback: Callable | None = None) -> Crew:
	llm = LLM(api_key=settings.GROQ_API_KEY, **crewai_model_kwargs(settings.GROQ_MODEL_DEFAULT))
	fetcher = create_news_fetcher_agent(llm)
	analyst = create_news_analyst_agent(llm, language, ai_tone)
	return Crew(agents=[fetcher, analyst], process=Process.sequential, verbose=True, step_callback=step_callback)


async def run_news_crew(
	user_message: str,
	conversation_history: list[dict],
	language: str,
	ai_tone: str,
	step_callback: Callable | None = None,
) -> str:
	crew = build_news_crew(language, ai_tone, step_callback=step_callback)
	fetcher_agent = crew.agents[0]
	analyst_agent = crew.agents[1]
	fetch_task = create_fetch_task(fetcher_agent, user_message, conversation_history)
	analysis_task = create_analysis_task(analyst_agent, fetch_task)
	crew.tasks = [fetch_task, analysis_task]
	result = await crew.kickoff_async()
	return result.raw
