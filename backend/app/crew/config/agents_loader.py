from __future__ import annotations

from pathlib import Path

import yaml
from crewai import Agent

from app.config import settings
from app.crew.llm_config import create_crewai_llm
from app.crew.tool_registry import registry
from app.crew.config.crew_schema import AgentsFileConfig


def _config_path() -> Path:
	return Path(__file__).with_name("agents.yaml")


def load_agent_configs() -> AgentsFileConfig:
	with _config_path().open("r", encoding="utf-8") as f:
		data = yaml.safe_load(f) or {}
	return AgentsFileConfig.model_validate(data)


def build_agents(*, language: str, ai_tone: str, default_model: str | None = None, reasoning_model: str | None = None) -> dict[str, Agent]:
	config = load_agent_configs()
	agents: dict[str, Agent] = {}
	for key, agent_cfg in config.agents.items():
		model_name = default_model or settings.GROQ_MODEL_DEFAULT
		if agent_cfg.llm_profile == "reasoning":
			model_name = reasoning_model or settings.GROQ_MODEL_REASONING
		goal = agent_cfg.goal.format(language=language, ai_tone=ai_tone)
		agent_kwargs = {
			"role": agent_cfg.role,
			"goal": goal,
			"backstory": agent_cfg.backstory,
			"tools": registry.create_tools(agent_cfg.tools),
			"llm": create_crewai_llm(model_name, temperature=0.3 if agent_cfg.llm_profile == "default" else None),
			"verbose": agent_cfg.verbose,
		}
		if agent_cfg.max_iter is not None:
			agent_kwargs["max_iter"] = agent_cfg.max_iter
		agents[key] = Agent(
			**agent_kwargs,
		)
	return agents
