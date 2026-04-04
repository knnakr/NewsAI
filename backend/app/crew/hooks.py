from __future__ import annotations

from crewai.events import crewai_event_bus
from crewai.events.types.tool_usage_events import ToolUsageStartedEvent
from crewai.events.types.tool_usage_events import ToolUsageFinishedEvent

from app.models.conversation import AgentToolCall
from app.crew.utils import _context_stack


def _emit_stream_event(event: dict) -> None:
    stream_queue = _context_stack.get("stream_queue")
    if stream_queue is None:
        return
    stream_queue.put_nowait(event)


@crewai_event_bus.on(ToolUsageStartedEvent)
async def on_tool_started(source, event: ToolUsageStartedEvent):
    if not _context_stack.get("message_id"):
        return

    _emit_stream_event({"event": "tool_start", "tool": event.tool_name, "args": event.tool_args})


@crewai_event_bus.on(ToolUsageFinishedEvent)
async def on_tool_used(source, event: ToolUsageFinishedEvent):
    if not _context_stack.get("message_id"):
        return

    message_id = _context_stack["message_id"]
    db = _context_stack["db"]
    known_tools = {
        "web_search",
        "fetch_news_by_category",
        "fetch_trending",
        "fact_check_search",
        "summarize_article",
    }

    tool_name = event.tool_name if event.tool_name in known_tools else None
    if tool_name is None:
        return

    tool_call = AgentToolCall(
        message_id=message_id,
        tool_name=tool_name,
        input_params=event.tool_input or {},
        output_result=str(event.tool_output),
        duration_ms=getattr(event, "duration_ms", None),
        is_success=not bool(getattr(event, "error", None)),
        error_message=str(event.error) if getattr(event, "error", None) else None,
    )
    db.add(tool_call)
    await db.commit()
    _emit_stream_event({"event": "tool_end", "tool": tool_name, "output": str(event.tool_output)})
