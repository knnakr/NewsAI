from __future__ import annotations

from crewai import Agent, LLM

from app.crew.tools.summarize import SummarizeArticleTool


def create_news_analyst_agent(llm: LLM, language: str, ai_tone: str) -> Agent:
	return Agent(
		role="News Analyst",
		goal=(
			f"Getirilen haberleri analiz et ve kullanıcıya {language} dilinde, "
			f"{ai_tone} tonunda, kaynaklı bir yanıt üret."
		),
		backstory=(
			"Sen tarafsız ve titiz bir haber analistsin. "
			"Her iddiayı kaynaklarla desteklersin, asla tahmin yürütmezsin."
		),
		tools=[SummarizeArticleTool()],
		llm=llm,
		verbose=True,
	)
