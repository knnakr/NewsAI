from __future__ import annotations

import asyncio

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import AsyncTavilyClient

from app.config import settings


class FactCheckSearchInput(BaseModel):
	claim: str = Field(description="Doğrulanacak iddia")


class FactCheckSearchTool(BaseTool):
	name: str = "fact_check_search"
	description: str = (
		"Bir iddiayı doğrulamak için özelleştirilmiş web araması yapar. "
		"Fact-checking için her zaman bu tool'u kullan."
	)
	args_schema: type[BaseModel] = FactCheckSearchInput

	def _run(self, claim: str) -> list[dict]:
		return asyncio.run(self._arun(claim=claim))

	async def _arun(self, claim: str) -> list[dict]:
		tavily = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
		response = await tavily.search(
			query=f"fact check: {claim}",
			search_depth="advanced",
			max_results=5,
			include_answer=True,
		)
		return [
			{"title": result["title"], "url": result["url"], "snippet": result["content"]}
			for result in response.get("results", [])
		]
