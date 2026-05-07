from mcp.types import Tool

from app.crew.tools.fetch_news import FetchNewsTool


 # Kategori bazlı haber toplama isteğini MCP üzerinden CrewAI tool'una yönlendirir.
def run(category: str, from_date: str | None = None) -> list[dict]:
    tool = FetchNewsTool()
    return tool._run(category=category, from_date=from_date)


 # Kategoriye göre haber çekme işlevini MCP istemcilerine açar.
fetch_news_adapter = Tool(
    name="fetch_news_by_category",
    description="Belirli bir kategoride haber makalelerini getirir.",
    inputSchema={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "Haber kategorisi",
                "enum": ["world", "technology", "sports", "economy", "health", "science", "entertainment"],
            },
            "from_date": {"type": "string", "description": "ISO tarih YYYY-MM-DD (opsiyonel)"},
        },
        "required": ["category"],
    },
)