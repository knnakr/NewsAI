from __future__ import annotations

from typing import Any

from crewai import LLM

from app.config import settings

GROQ_OPENAI_BASE_URL = "https://api.groq.com/openai/v1"
_COMPOUND_MODELS = {"groq/compound", "groq/compound-mini"}


 # Model adını LiteLLM/Groq uyumlu standart önek formatına normalleştirir.
def normalize_groq_model(model_name: str) -> str:
	return model_name if model_name.startswith("groq/") else f"groq/{model_name}"


 # CrewAI LLM istemcisi için modele göre gerekli sağlayıcı parametrelerini üretir.
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


 # API anahtarı ve model parametreleriyle CrewAI LLM nesnesini oluşturur.
def create_crewai_llm(model_name: str, temperature: float | None = None) -> LLM:
	kwargs = crewai_model_kwargs(model_name)
	if temperature is not None:
		kwargs["temperature"] = temperature
	return LLM(api_key=settings.GROQ_API_KEY, **kwargs)
