from __future__ import annotations

import asyncio
import httpx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SummarizeInput(BaseModel):
	url: str = Field(description="Özetlenecek haber URL'i")


class SummarizeArticleTool(BaseTool):
	name: str = "summarize_article"
	description: str = "Verilen URL'deki makaleyi çekip 3-4 cümlelik özet üretir."
	args_schema: type[BaseModel] = SummarizeInput

	def _run(self, url: str) -> str:
		return asyncio.run(self._arun(url=url))

	async def _arun(self, url: str) -> str:
		try:
			async with httpx.AsyncClient(timeout=10.0) as client:
				response = await client.get(url, follow_redirects=True)
				text = response.text[:5000]
				return text
		except Exception as exc:
			return f"Makale yüklenemedi, hata: {str(exc)}"
