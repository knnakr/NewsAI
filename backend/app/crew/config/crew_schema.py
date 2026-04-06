from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
	role: str
	goal: str
	backstory: str
	tools: list[str] = Field(default_factory=list)
	llm_profile: Literal["default", "reasoning"] = "default"
	max_iter: int | None = None
	verbose: bool = True


class AgentsFileConfig(BaseModel):
	agents: dict[str, AgentConfig]


class TaskConfig(BaseModel):
	description: str
	expected_output: str
	agent_ref: str
	context: list[str] = Field(default_factory=list)


class TasksFileConfig(BaseModel):
	tasks: dict[str, TaskConfig]


class CrewConfig(BaseModel):
	agents: list[str]
	tasks: list[str]
	process: Literal["sequential"] = "sequential"
	verbose: bool = True


class CrewsFileConfig(BaseModel):
	crews: dict[str, CrewConfig]
