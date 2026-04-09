from __future__ import annotations

from collections.abc import Callable

from crewai import Crew

from app.crew.config.agents_loader import build_agents
from app.crew.config.crews_loader import build_crews
from app.crew.config.tasks_loader import build_tasks


class CrewFactory:
	"""Builds all CrewAI flows from YAML configuration."""

	@staticmethod
	def create_news_crew(
		*,
		user_message: str,
		conversation_history: list[dict],
		language: str,
		ai_tone: str,
		step_callback: Callable | None = None,
	) -> Crew:
		agents = build_agents(language=language, ai_tone=ai_tone)
		tasks = build_tasks(
			agents=agents,
			user_message=user_message,
			conversation_history=conversation_history,
			language=language,
			ai_tone=ai_tone,
		)
		crews = build_crews(agents=agents, tasks=tasks, step_callback=step_callback)
		return crews["news"]

	@staticmethod
	def create_fact_check_crew(
		*,
		claim: str,
		default_model: str | None = None,
		reasoning_model: str | None = None,
	) -> Crew:
		agents = build_agents(
			language="Turkish",
			ai_tone="neutral",
			default_model=default_model,
			reasoning_model=reasoning_model,
		)
		tasks = build_tasks(agents=agents, claim=claim)
		crews = build_crews(agents=agents, tasks=tasks)
		return crews["fact_check"]

	@staticmethod
	def create_news_summary_crew(
		*,
		article_url: str,
		article_title: str,
		article_source: str,
		article_category: str,
		language: str = "Turkish",
		ai_tone: str = "neutral",
	) -> Crew:
		agents = build_agents(language=language, ai_tone=ai_tone)
		tasks = build_tasks(
			agents=agents,
			article_url=article_url,
			article_title=article_title,
			article_source=article_source,
			article_category=article_category,
			language=language,
			ai_tone=ai_tone,
		)
		crews = build_crews(agents=agents, tasks=tasks)
		return crews["summarize_news"]
