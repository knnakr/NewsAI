from __future__ import annotations

from typing import Any

GROQ_OPENAI_BASE_URL = "https://api.groq.com/openai/v1"
_COMPOUND_MODELS = {"groq/compound", "groq/compound-mini"}


def normalize_groq_model(model_name: str) -> str:
	return model_name if model_name.startswith("groq/") else f"groq/{model_name}"


def crewai_model_kwargs(model_name: str) -> dict[str, Any]:
	"""Build CrewAI/LiteLLM kwargs for a Groq model.

	Compound models require OpenAI-provider routing in LiteLLM to preserve
	the full model id (e.g. groq/compound-mini) instead of stripping it.
	"""
	normalized = normalize_groq_model(model_name)
	if normalized in _COMPOUND_MODELS:
		return {
			"model": f"openai/{normalized}",
			"base_url": GROQ_OPENAI_BASE_URL,
		}
	return {"model": normalized}
