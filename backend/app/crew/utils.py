from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

_context_stack: dict = {}


def set_tool_call_context(
    message_id: UUID,
    db: AsyncSession,
    user_id: UUID | None,
    stream_queue: object | None = None,
):
    """Store request-scoped context for CrewAI tool-call logging hooks."""
    _context_stack["message_id"] = message_id
    _context_stack["db"] = db
    _context_stack["user_id"] = user_id
    if stream_queue is not None:
        _context_stack["stream_queue"] = stream_queue


def clear_tool_call_context():
    _context_stack.clear()
