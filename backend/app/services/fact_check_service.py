import asyncio
import json
import os
import re
import uuid
from typing import Any, Literal, TypedDict

from groq import AsyncGroq
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crew.crew_factory import CrewFactory
from app.crew.tools.fact_check_search import FactCheckSearchTool
from app.crew.tools.web_search import WebSearchTool
from app.models.fact_check import FactCheck
from app.models.user import UserPreferences
from app.schemas.fact_check import FactCheckResponse


Orchestrator = Literal["crewai", "langgraph"]


class FactCheckResultPayload(BaseModel):
	verdict: Literal["TRUE", "FALSE", "UNVERIFIED"]
	explanation: str = Field(min_length=1)
	confidence_score: float = Field(ge=0.0, le=1.0)
	sources: list[dict[str, Any]] = Field(default_factory=list)


class FactCheckGraphState(TypedDict, total=False):
	claim: str
	research_sources: list[dict[str, Any]]
	verdict_payload: dict[str, Any]


async def check_claim(claim: str, user_id: uuid.UUID | None, db: AsyncSession) -> FactCheck:
	orchestrator = await _resolve_fact_check_orchestrator(user_id=user_id, db=db)
	result = await _run_fact_check(claim=claim, orchestrator=orchestrator)
	fact_check = FactCheck(
		user_id=user_id,
		claim=claim,
		verdict=result["verdict"],
		explanation=result["explanation"],
		confidence_score=result["confidence_score"],
		sources=result.get("sources", []),
	)
	db.add(fact_check)
	await db.commit()
	await db.refresh(fact_check)
	# Ensure DB entity always remains response-compatible for API stability.
	FactCheckResponse.model_validate(fact_check)
	return fact_check


async def _resolve_fact_check_orchestrator(*, user_id: uuid.UUID | None, db: AsyncSession) -> Orchestrator:
	# Global safety switch: when disabled, always use CrewAI regardless of user preference.
	if not settings.ENABLE_LANGGRAPH:
		return "crewai"

	if user_id is None:
		return "crewai"

	preferences = await db.get(UserPreferences, user_id)
	orchestrator = getattr(preferences, "orchestrator", None)
	if orchestrator in {"crewai", "langgraph"}:
		return orchestrator

	return "crewai"


async def _run_fact_check(*, claim: str, orchestrator: Orchestrator) -> dict:
	try:
		if orchestrator == "langgraph":
			return await _run_fact_check_with_langgraph(claim)

		return await _run_fact_check_with_retry(claim)
	except Exception as exc:
		if not _is_known_upstream_ai_error(exc):
			raise
		return _build_unverified_fallback_payload(exc)


async def _run_fact_check_with_langgraph(claim: str) -> dict:
	_apply_langsmith_env()
	graph = _build_fact_check_graph()
	state = await graph.ainvoke(
		{"claim": claim},
		config={"recursion_limit": settings.LANGGRAPH_RECURSION_LIMIT},
	)
	payload = state.get("verdict_payload")
	if payload is None:
		raise ValueError("LangGraph fact-check did not produce a verdict payload")
	return _validate_fact_check_payload(payload)


def _build_fact_check_graph():
	workflow = StateGraph(FactCheckGraphState)
	workflow.add_node("research_claim", _research_claim_node)
	workflow.add_node("produce_verdict", _produce_verdict_node)
	workflow.add_edge(START, "research_claim")
	workflow.add_edge("research_claim", "produce_verdict")
	workflow.add_edge("produce_verdict", END)
	return workflow.compile()


async def _research_claim_node(state: FactCheckGraphState) -> FactCheckGraphState:
	claim = state["claim"]
	fact_tool = FactCheckSearchTool()
	web_tool = WebSearchTool()

	fact_sources, web_sources = await asyncio.gather(
		fact_tool._arun(claim=claim),
		web_tool._arun(query=f"fact check: {claim}", max_results=5),
	)

	merged_sources = _deduplicate_sources([*fact_sources, *web_sources])
	return {"research_sources": merged_sources[:8]}


async def _produce_verdict_node(state: FactCheckGraphState) -> FactCheckGraphState:
	claim = state["claim"]
	research_sources = state.get("research_sources", [])

	if not research_sources:
		return {
			"verdict_payload": {
				"verdict": "UNVERIFIED",
				"explanation": "Yeterli bagimsiz kaynak bulunamadi.",
				"confidence_score": 0.2,
				"sources": [],
			}
		}

	client = AsyncGroq(api_key=settings.GROQ_API_KEY)
	prompt = (
		"You are a strict fact-checking judge. Evaluate the claim using the provided sources only. "
		"Return JSON with keys: verdict, explanation, confidence_score, sources. "
		"Allowed verdict values: TRUE, FALSE, UNVERIFIED. "
		"Keep explanation short (2-3 sentences). confidence_score must be between 0 and 1."
	)

	model_name = _normalize_groq_chat_model(settings.GROQ_MODEL_REASONING)
	response = await client.chat.completions.create(
		model=model_name,
		temperature=0.1,
		response_format={"type": "json_object"},
		messages=[
			{"role": "system", "content": prompt},
			{
				"role": "user",
				"content": (
					f"Claim: {claim}\n"
					f"Sources JSON: {json.dumps(research_sources, ensure_ascii=False)}"
				),
			},
		],
	)

	content = response.choices[0].message.content or "{}"
	payload = _normalize_fact_check_output(content)
	payload.setdefault("sources", research_sources[:5])
	return {"verdict_payload": payload}


async def _run_fact_check_with_retry(claim: str) -> dict:
	max_attempts = 5
	for attempt in range(max_attempts):
		try:
			crew = CrewFactory.create_fact_check_crew(claim=claim)
			result = await crew.kickoff_async()
			return _normalize_fact_check_output(result.raw)
		except Exception as exc:
			if _needs_compound_fallback(exc):
				crew = CrewFactory.create_fact_check_crew(
					claim=claim,
					default_model=settings.GROQ_MODEL_DEFAULT,
					reasoning_model=settings.GROQ_MODEL_REASONING,
				)
				result = await crew.kickoff_async()
				return _normalize_fact_check_output(result.raw)
			if not (_is_rate_limit_error(exc) or _is_transient_llm_response_error(exc)) or attempt == max_attempts - 1:
				raise
			await asyncio.sleep(_extract_retry_after_seconds(exc))

	raise RuntimeError("Fact-check crew unexpectedly failed without an exception")


def _is_rate_limit_error(exc: Exception) -> bool:
	message = str(exc).lower()
	return "rate_limit_exceeded" in message or "ratelimiterror" in message


def _is_transient_llm_response_error(exc: Exception) -> bool:
	message = str(exc).lower()
	return (
		"invalid response from llm call - none or empty" in message
		or "received none or empty response from llm call" in message
	)


def _is_known_upstream_ai_error(exc: Exception) -> bool:
	message = str(exc).lower()
	return (
		_is_rate_limit_error(exc)
		or _is_transient_llm_response_error(exc)
		or "request_too_large" in message
		or "request entity too large" in message
		or "model_not_found" in message
		or "does not exist or you do not have access" in message
		or "timeout" in message
	)


def _build_unverified_fallback_payload(exc: Exception) -> dict[str, Any]:
	message = str(exc).strip()
	if len(message) > 240:
		message = message[:240]
	return {
		"verdict": "UNVERIFIED",
		"explanation": f"AI yaniti gecici olarak alinamadi. Lütfen tekrar deneyin. Detay: {message}",
		"confidence_score": 0.2,
		"sources": [],
	}


def _needs_compound_fallback(exc: Exception) -> bool:
	message = str(exc).lower()
	return (
		"last message role must be 'user'" in message
		or "request entity too large" in message
		or "request_too_large" in message
		or "model_not_found" in message
		or "does not exist or you do not have access" in message
	)


def _extract_retry_after_seconds(exc: Exception) -> float:
	message = str(exc)
	match = re.search(r"try again in\s+([0-9]+(?:\.[0-9]+)?)s", message, flags=re.IGNORECASE)
	if not match:
		return 3.0
	try:
		return min(float(match.group(1)) + 0.5, 8.0)
	except ValueError:
		return 3.0


def _normalize_fact_check_output(raw: object) -> dict:
	if isinstance(raw, dict):
		return _validate_fact_check_payload(raw)
	if isinstance(raw, str):
		clean = raw.strip()
		if clean.startswith("```"):
			clean = re.sub(r"^```[a-zA-Z]*", "", clean).strip()
			clean = re.sub(r"```$", "", clean).strip()
		return _validate_fact_check_payload(json.loads(clean))
	raise ValueError("Fact-check crew returned unsupported output format")


def _validate_fact_check_payload(payload: dict[str, Any]) -> dict[str, Any]:
	payload = dict(payload)
	payload["sources"] = _coerce_sources(payload.get("sources", []))
	validated = FactCheckResultPayload.model_validate(payload)
	return validated.model_dump()


def _coerce_sources(raw_sources: Any) -> list[dict[str, Any]]:
	if raw_sources is None:
		return []
	if not isinstance(raw_sources, list):
		raw_sources = [raw_sources]

	coerced: list[dict[str, Any]] = []
	for item in raw_sources:
		if isinstance(item, dict):
			url = str(item.get("url", "")).strip()
			title = str(item.get("title", "")).strip()
			snippet = str(item.get("snippet", item.get("content", ""))).strip()
			if not url and not title and not snippet:
				continue
			coerced.append({"title": title, "url": url, "snippet": snippet})
			continue

		text = str(item).strip()
		if not text:
			continue
		if text.startswith("http://") or text.startswith("https://"):
			coerced.append({"title": "", "url": text, "snippet": ""})
		else:
			coerced.append({"title": "", "url": "", "snippet": text})

	return coerced


def _deduplicate_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
	seen_urls: set[str] = set()
	result: list[dict[str, Any]] = []
	for source in sources:
		url = str(source.get("url", "")).strip()
		if not url or url in seen_urls:
			continue
		seen_urls.add(url)
		result.append(
			{
				"title": str(source.get("title", ""))[:300],
				"url": url,
				"snippet": str(source.get("snippet", source.get("content", "")))[:1000],
			}
		)
	return result


def _normalize_groq_chat_model(model_name: str) -> str:
	return model_name.removeprefix("groq/")


def _apply_langsmith_env() -> None:
	if not settings.LANGSMITH_TRACING:
		return

	os.environ["LANGSMITH_TRACING"] = "true"
	os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
	os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
	if settings.LANGSMITH_API_KEY:
		os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
