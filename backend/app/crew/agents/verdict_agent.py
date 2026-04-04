from __future__ import annotations

from crewai import Agent, LLM

from app.config import settings
from app.crew.llm_config import crewai_model_kwargs


def create_verdict_agent(llm: LLM, reasoning_model: str | None = None) -> Agent:
	return Agent(
		role="Verdict Agent",
		goal="Araştırma bulgularını değerlendirip yapılandırılmış karar ver.",
		backstory=(
			"Sen tarafsız bir hakem ve editörsün. "
			"Kanıtlara dayanarak TRUE/FALSE/UNVERIFIED kararı verirsin. "
			"Asla tahmin yapmazsın; kanıt yetersizse UNVERIFIED döndürürsün."
		),
		tools=[],
		llm=LLM(
			api_key=settings.GROQ_API_KEY,
			**crewai_model_kwargs(reasoning_model or settings.GROQ_MODEL_REASONING),
		),
	)
