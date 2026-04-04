from __future__ import annotations

from crewai import Agent, LLM

from app.crew.tools.fact_check_search import FactCheckSearchTool
from app.crew.tools.web_search import WebSearchTool


def create_fact_checker_agent(llm: LLM) -> Agent:
	return Agent(
		role="Fact Checker",
		goal="İddiayı birden fazla bağımsız kaynakta araştır.",
		backstory=(
			"Sen şüpheci ve titiz bir araştırmacısın. "
			"Her iddiayı en az iki bağımsız kaynakla doğrularsın."
		),
		tools=[FactCheckSearchTool(), WebSearchTool()],
		llm=llm,
		max_iter=3,
	)
