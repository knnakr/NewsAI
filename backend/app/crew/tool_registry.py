from __future__ import annotations

from collections.abc import Callable

from crewai.tools import BaseTool

from app.crew.tools.fact_check_search import FactCheckSearchTool
from app.crew.tools.fetch_news import FetchNewsTool
from app.crew.tools.fetch_trending import FetchTrendingTool
from app.crew.tools.summarize import SummarizeArticleTool
from app.crew.tools.web_search import WebSearchTool


class ToolRegistry:
	"""Resolves YAML tool names to concrete tool instances."""

	def __init__(self) -> None:
		self._tool_factories: dict[str, Callable[[], BaseTool]] = {
			"web_search": WebSearchTool,
			"fetch_news_by_category": FetchNewsTool,
			"fetch_trending": FetchTrendingTool,
			"fact_check_search": FactCheckSearchTool,
			"summarize_article": SummarizeArticleTool,
		}

	def create_tools(self, names: list[str]) -> list[BaseTool]:
		tools: list[BaseTool] = []
		for name in names:
			factory = self._tool_factories.get(name)
			if factory is None:
				raise ValueError(f"Unknown tool in YAML config: {name}")
			tools.append(factory())
		return tools

	@property
	def available_tools(self) -> set[str]:
		return set(self._tool_factories.keys())


registry = ToolRegistry()
