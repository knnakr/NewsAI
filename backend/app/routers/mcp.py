from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.mcp.server import TOOLS, call_tool

router = APIRouter(prefix="/mcp", tags=["mcp"])


class ToolCallRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str
    method: str
    params: dict | None = None


@router.get("/health")
# MCP katmanının erişilebilir olduğunu doğrulayan hafif sağlık endpointidir.
async def health():
    return {"status": "ok", "server": "newsai-mcp"}


@router.get("/tools")
# Kayıtlı MCP tool listesini şema bilgileriyle birlikte istemciye sunar.
async def list_tools():
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema,
            }
            for tool in TOOLS
        ]
    }


@router.post("")
# JSON-RPC formatındaki tools/call isteğini doğrulayıp ilgili tool'u çalıştırır.
async def call_mcp_tool(request: ToolCallRequest):
    if request.method != "tools/call":
        raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")

    if not request.params:
        raise HTTPException(status_code=400, detail="Missing params")

    tool_name = request.params.get("name")
    arguments = request.params.get("arguments", {})

    if not tool_name:
        raise HTTPException(status_code=400, detail="Missing tool name")

    try:
        result = await call_tool(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "content": [{"type": "text", "text": r.text} for r in result]
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))