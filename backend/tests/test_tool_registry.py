from app.crew.tool_registry import registry


def test_tool_registry_has_expected_tools():
	expected = {
		"web_search",
		"fetch_news_by_category",
		"fetch_trending",
		"fact_check_search",
		"summarize_article",
	}
	assert expected.issubset(registry.available_tools)


def test_tool_registry_creates_tool_instances():
	tools = registry.create_tools(["web_search", "summarize_article"])
	tool_names = [tool.name for tool in tools]
	assert tool_names == ["web_search", "summarize_article"]
