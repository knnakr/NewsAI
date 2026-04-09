from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml
from crewai import Task

from app.crew.config.crew_schema import TasksFileConfig


class _StrictFormatDict(dict):
	def __missing__(self, key: str):
		raise KeyError(f"Missing template variable in task config: {key}")


def _config_path() -> Path:
	return Path(__file__).with_name("tasks.yaml")


def load_task_configs() -> TasksFileConfig:
	with _config_path().open("r", encoding="utf-8") as f:
		data = yaml.safe_load(f) or {}
	return TasksFileConfig.model_validate(data)


def build_tasks(
	*,
	agents: dict,
	user_message: str = "",
	conversation_history: list[dict] | None = None,
	claim: str = "",
	article_url: str = "",
	article_title: str = "",
	article_source: str = "",
	article_category: str = "",
	language: str = "Turkish",
	ai_tone: str = "neutral",
) -> dict[str, Task]:
	config = load_task_configs()
	history = conversation_history or []
	history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-10:]])
	now_utc = datetime.now(timezone.utc)
	template_values = _StrictFormatDict(
		user_message=user_message,
		conversation_history_text=history_text,
		claim=claim,
		article_url=article_url,
		article_title=article_title,
		article_source=article_source,
		article_category=article_category,
		language=language,
		ai_tone=ai_tone,
		current_date=now_utc.date().isoformat(),
		current_year=str(now_utc.year),
	)
	tasks: dict[str, Task] = {}
	context_refs: dict[str, list[str]] = {}

	for key, task_cfg in config.tasks.items():
		agent = agents[task_cfg.agent_ref]
		description = task_cfg.description.format_map(template_values)
		expected_output = task_cfg.expected_output.format_map(template_values)
		tasks[key] = Task(
			description=description,
			expected_output=expected_output,
			agent=agent,
		)
		context_refs[key] = task_cfg.context

	for key, refs in context_refs.items():
		tasks[key].context = [tasks[ref] for ref in refs]

	return tasks
