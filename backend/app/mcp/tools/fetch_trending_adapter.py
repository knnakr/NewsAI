from mcp.types import Tool

from app.crew.tools.fetch_trending import FetchTrendingTool


 # Trend haber isteğini MCP çağrısından CrewAI trending tool'una aktarır.
def run(topic: str | None = None) -> list[dict]:
    tool = FetchTrendingTool()
    return tool._run(topic=topic)


 # Trend haber toplama işlevini MCP tool listesine kaydeder.
fetch_trending_adapter = Tool(
    name="fetch_trending",
    description="Trend haberleri getirir.",
    inputSchema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Trend konusu (opsiyonel)",
                "enum": ["world", "technology", "sports", "economy", "health", "science", "entertainment"],
            },
        },
        "required": [],
    },
)