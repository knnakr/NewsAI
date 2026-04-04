from __future__ import annotations

import json

from crewai import Crew, LLM, Process

from app.config import settings
from app.crew.agents.fact_checker import create_fact_checker_agent
from app.crew.agents.verdict_agent import create_verdict_agent
from app.crew.llm_config import crewai_model_kwargs
from app.crew.tasks.fact_check_tasks import create_research_task, create_verdict_task


async def run_fact_check_crew(
	claim: str,
	default_model: str | None = None,
	reasoning_model: str | None = None,
) -> dict:
	default_model_name = default_model or settings.GROQ_MODEL_DEFAULT
	reasoning_model_name = reasoning_model or settings.GROQ_MODEL_REASONING
	llm = LLM(api_key=settings.GROQ_API_KEY, **crewai_model_kwargs(default_model_name))
	checker = create_fact_checker_agent(llm)
	verdict = create_verdict_agent(llm, reasoning_model=reasoning_model_name)
	research_task = create_research_task(checker, claim)
	verdict_task = create_verdict_task(verdict, research_task)
	crew = Crew(
		agents=[checker, verdict],
		tasks=[research_task, verdict_task],
		process=Process.sequential,
		verbose=True,
	)
	result = await crew.kickoff_async()
	return json.loads(result.raw)
