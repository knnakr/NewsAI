from __future__ import annotations

from pathlib import Path

import yaml
from crewai import Crew, Process

from app.crew.config.crew_schema import CrewsFileConfig


def _config_path() -> Path:
	return Path(__file__).with_name("crews.yaml")


def load_crew_configs() -> CrewsFileConfig:
	with _config_path().open("r", encoding="utf-8") as f:
		data = yaml.safe_load(f) or {}
	return CrewsFileConfig.model_validate(data)


def build_crews(*, agents: dict, tasks: dict, step_callback=None) -> dict[str, Crew]:
	config = load_crew_configs()
	crews: dict[str, Crew] = {}
	for key, crew_cfg in config.crews.items():
		crews[key] = Crew(
			agents=[agents[name] for name in crew_cfg.agents],
			tasks=[tasks[name] for name in crew_cfg.tasks],
			process=Process.sequential,
			verbose=crew_cfg.verbose,
			step_callback=step_callback,
		)
	return crews
