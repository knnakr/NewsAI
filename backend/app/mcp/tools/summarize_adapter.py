from mcp.types import Tool

from app.crew.tools.summarize import SummarizeArticleTool


 # Makale özetleme çağrısını MCP katmanından CrewAI özetleme tool'una iletir.
def run(url: str) -> str:
    tool = SummarizeArticleTool()
    return tool._run(url=url)


 # URL tabanlı makale özetleme yeteneğini MCP üzerinden yayınlar.
summarize_adapter = Tool(
    name="summarize_article",
    description="Verilen URL'deki makaleyi çekip içeriğini döndürür.",
    inputSchema={
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Özetlenecek haber URL'i"},
        },
        "required": ["url"],
    },
)