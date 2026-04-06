import asyncio
import json
import re
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crew.crew_factory import CrewFactory
from app.models.fact_check import FactCheck


async def check_claim(claim: str, user_id: uuid.UUID | None, db: AsyncSession) -> FactCheck:
	result = await _run_fact_check_with_retry(claim)
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
	return fact_check


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
			if not _is_rate_limit_error(exc) or attempt == max_attempts - 1:
				raise
			await asyncio.sleep(_extract_retry_after_seconds(exc))

	raise RuntimeError("Fact-check crew unexpectedly failed without an exception")


def _is_rate_limit_error(exc: Exception) -> bool:
	message = str(exc).lower()
	return "rate_limit_exceeded" in message or "ratelimiterror" in message


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
		return raw
	if isinstance(raw, str):
		return json.loads(raw)
	raise ValueError("Fact-check crew returned unsupported output format")
