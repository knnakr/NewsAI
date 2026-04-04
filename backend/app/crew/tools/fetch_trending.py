from __future__ import annotations

import asyncio
from typing import Literal

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.services.news_service import get_trending_articles


class FetchTrendingInput(BaseModel):
	topic: Literal[
		"world",
		"technology",
		"sports",
		"economy",
		"health",
		"science",
		"entertainment",
	] | None = Field(default=None, description="Trend konusu")


class FetchTrendingTool(BaseTool):
	name: str = "fetch_trending"
	description: str = "Trend haberleri getirir. Kullanıcı trending haberleri istediğinde kullan."
	args_schema: type[BaseModel] = FetchTrendingInput

	async def _arun(self, topic: str | None = None) -> list[dict]:
		return await get_trending_articles(topic=topic)

	def _run(self, topic: str | None = None) -> list[dict]:
		return asyncio.run(self._arun(topic=topic))
