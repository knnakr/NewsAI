from mcp.types import Tool

from app.crew.tools.fact_check_search import FactCheckSearchTool


 # MCP çağrısını CrewAI fact-check arama tool'una köprüleyerek çalıştırır.
def run(claim: str) -> list[dict]:
    tool = FactCheckSearchTool()
    return tool._run(claim=claim)


 # Fact-check aramasını MCP istemcilerine açan tool tanımıdır.
fact_check_adapter = Tool(
    name="fact_check_search",
    description="Bir iddiayı doğrulamak için web araması yapar. Fact-checking için kullan.",
    inputSchema={
        "type": "object",
        "properties": {
            "claim": {"type": "string", "description": "Doğrulanacak iddia"},
        },
        "required": ["claim"],
    },
)