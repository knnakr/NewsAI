from mcp.types import Tool

from app.crew.tools.web_search import WebSearchTool


 # MCP'den gelen web arama isteğini CrewAI web arama tool'u ile yürütür.
def run(query: str, max_results: int = 5) -> list[dict]:
    tool = WebSearchTool()
    return tool._run(query=query, max_results=max_results)


 # Genel web arama yeteneğini MCP tool kataloğuna ekler.
web_search_adapter = Tool(
    name="web_search",
    description="Web'de güncel haber, olay veya bilgi arar. Son gelişmeler için kullan.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Arama sorgusu"},
            "max_results": {"type": "integer", "description": "Maksimum sonuç sayısı", "default": 5},
        },
        "required": ["query"],
    },
)