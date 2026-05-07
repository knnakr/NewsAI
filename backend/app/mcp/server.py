import asyncio

from mcp.server import Server
from mcp.types import Tool, TextContent

from app.mcp.tools.fact_check_adapter import fact_check_adapter
from app.mcp.tools.web_search_adapter import web_search_adapter
from app.mcp.tools.summarize_adapter import summarize_adapter
from app.mcp.tools.fetch_news_adapter import fetch_news_adapter
from app.mcp.tools.fetch_trending_adapter import fetch_trending_adapter

server = Server(
    name="newsai-mcp",
    version="1.0.0",
    instructions="NewsAI MCP Server - Haber AI asistanı için MCP sunucusu",
)

# MCP üstünden dışa açılacak tüm tool adapter tanımlarını merkezi olarak tutar.
TOOLS = [
    fact_check_adapter,
    web_search_adapter,
    summarize_adapter,
    fetch_news_adapter,
    fetch_trending_adapter,
]


 # Tool çağrısını ada göre çözümler ve sonucu MCP TextContent listesine dönüştürür.
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "fact_check_search":
        from app.mcp.tools.fact_check_adapter import run as run_fact_check
        result = await asyncio.to_thread(run_fact_check, **arguments)
        return [TextContent(type="text", text=str(result))]
    elif name == "web_search":
        from app.mcp.tools.web_search_adapter import run as run_web_search
        result = await asyncio.to_thread(run_web_search, **arguments)
        return [TextContent(type="text", text=str(result))]
    elif name == "summarize_article":
        from app.mcp.tools.summarize_adapter import run as run_summarize
        result = await asyncio.to_thread(run_summarize, **arguments)
        return [TextContent(type="text", text=str(result))]
    elif name == "fetch_news_by_category":
        from app.mcp.tools.fetch_news_adapter import run as run_fetch_news
        result = await asyncio.to_thread(run_fetch_news, **arguments)
        return [TextContent(type="text", text=str(result))]
    elif name == "fetch_trending":
        from app.mcp.tools.fetch_trending_adapter import run as run_fetch_trending
        result = await asyncio.to_thread(run_fetch_trending, **arguments)
        return [TextContent(type="text", text=str(result))]
    else:
        raise ValueError(f"Unknown tool: {name}")
