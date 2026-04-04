from __future__ import annotations

import asyncio

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import AsyncTavilyClient

from app.config import settings


class WebSearchInput(BaseModel):
	query: str = Field(description="Arama sorgusu")
	max_results: int = Field(default=5)


class WebSearchTool(BaseTool):
	name: str = "web_search"
	description: str = (
		"Web'de güncel haber, olay veya bilgi arar. "
		"Son gelişmeler için kullan."
	)
	args_schema: type[BaseModel] = WebSearchInput

	def _run(self, query: str, max_results: int = 5) -> list[dict]:
		return asyncio.run(self._arun(query=query, max_results=max_results))

	async def _arun(self, query: str, max_results: int = 5) -> list[dict]:
		tavily = AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)
		response = await tavily.search(
			query=query,
			search_depth="advanced",
			max_results=max_results,
			include_answer=True,
		)
		return [
			{"title": result["title"], "url": result["url"], "snippet": result["content"]}
			for result in response.get("results", [])
		]
