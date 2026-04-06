from __future__ import annotations

import asyncio
from collections.abc import Callable
import re
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.crew.crew_factory import CrewFactory
from app.crew.utils import clear_tool_call_context, set_tool_call_context


async def kickoff_with_tool_context(*, crew, message_id: UUID, db, user_id: UUID | None = None):
	"""Run crew kickoff with tool-call context lifecycle management."""
	set_tool_call_context(message_id, db, user_id)
	try:
		result = await crew.kickoff_async()
	finally:
		clear_tool_call_context()
	return result


async def run_chat_crew(
	user_message: str,
	conversation_history: list[dict],
	user_preferences: dict,
	db: AsyncSession,
	message_id: UUID,
	step_callback: Callable | None = None,
	stream_queue: object | None = None,
) -> tuple[str, list[dict]]:
	if _is_simple_greeting(user_message):
		return (
			"Merhaba! Size guncel haberleri bulabilir, bir konuyu ozetleyebilir veya bir iddiayi dogrulamada yardimci olabilirim."
			" Ne ogrenmek istersiniz?",
			[],
		)

	language = user_preferences.get("language", "Turkish")
	ai_tone = user_preferences.get("ai_tone", "neutral")

	set_tool_call_context(message_id, db, None, stream_queue=stream_queue)
	try:
		result = await _run_news_crew_with_retry(
			user_message=user_message,
			conversation_history=conversation_history,
			language=language,
			ai_tone=ai_tone,
			step_callback=step_callback,
		)
	finally:
		clear_tool_call_context()

	sources = _parse_sources_from_result(result)
	return result, sources


async def _run_news_crew_with_retry(
	*,
	user_message: str,
	conversation_history: list[dict],
	language: str,
	ai_tone: str,
	step_callback: Callable | None,
) -> str:
	# Groq on-demand tier can briefly rate-limit on TPM; retry with short backoff.
	max_attempts = 3
	for attempt in range(max_attempts):
		try:
			crew = CrewFactory.create_news_crew(
				user_message=user_message,
				conversation_history=conversation_history,
				language=language,
				ai_tone=ai_tone,
				step_callback=step_callback,
			)
			result = await crew.kickoff_async()
			return result.raw
		except Exception as exc:
			if not _is_rate_limit_error(exc) or attempt == max_attempts - 1:
				raise
			await asyncio.sleep(_extract_retry_after_seconds(exc))

	# Defensive fallback; loop always returns or raises.
	raise RuntimeError("News crew unexpectedly failed without an exception")


def _is_rate_limit_error(exc: Exception) -> bool:
	message = str(exc).lower()
	return "rate_limit_exceeded" in message or "ratelimiterror" in message


def _extract_retry_after_seconds(exc: Exception) -> float:
	message = str(exc)
	match = re.search(r"try again in\s+([0-9]+(?:\.[0-9]+)?)s", message, flags=re.IGNORECASE)
	if not match:
		return 3.0
	try:
		# add a small buffer to avoid immediate re-hit
		return min(float(match.group(1)) + 0.5, 8.0)
	except ValueError:
		return 3.0


def _is_simple_greeting(user_message: str) -> bool:
	text = user_message.strip().lower()
	if not text:
		return False

	greetings = {
		"hi",
		"hello",
		"hey",
		"selam",
		"merhaba",
		"sa",
		"slm",
		"yo",
	}

	return text in greetings


def _parse_sources_from_result(result: str) -> list[dict]:
	"""Extract URLs from markdown/plain text crew output as source list."""
	urls = re.findall(r"https?://[^\s\)]+", result)
	return [{"url": url} for url in urls[:10]]
