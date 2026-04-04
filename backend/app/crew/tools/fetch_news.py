from __future__ import annotations

import asyncio
from typing import Literal

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.services.news_service import get_or_fetch_articles


class FetchNewsInput(BaseModel):
	category: Literal[
		"world",
		"technology",
		"sports",
		"economy",
		"health",
		"science",
		"entertainment",
	] = Field(description="Haber kategorisi")
	from_date: str | None = Field(default=None, description="ISO tarih YYYY-MM-DD")


class FetchNewsTool(BaseTool):
	name: str = "fetch_news_by_category"
	description: str = (
		"Belirli bir kategoride yapılandırılmış haber makalelerini getirir. "
		"Kullanıcı belirli bir konuda haber istediğinde kullan."
	)
	args_schema: type[BaseModel] = FetchNewsInput

	async def _arun(self, category: str, from_date: str | None = None) -> list[dict]:
		allowed_categories = {
			"world",
			"technology",
			"sports",
			"economy",
			"health",
			"science",
			"entertainment",
		}
		if category not in allowed_categories:
			raise ValueError("Geçersiz kategori")
		return await get_or_fetch_articles(category, from_date=from_date)

	def _run(self, category: str, from_date: str | None = None) -> list[dict]:
		return asyncio.run(self._arun(category=category, from_date=from_date))
