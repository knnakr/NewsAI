import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.user import Base

if TYPE_CHECKING:
	from app.models.user import User


class Conversation(Base):
	__tablename__ = "conversations"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	title: Mapped[str | None] = mapped_column(Text, nullable=True)
	is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
		onupdate=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="conversations")
	messages: Mapped[list["Message"]] = relationship(
		back_populates="conversation",
		cascade="all, delete",
	)


class Message(Base):
	__tablename__ = "messages"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	conversation_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("conversations.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	role: Mapped[str] = mapped_column(
		SAEnum("user", "assistant", "system", name="message_role"),
		nullable=False,
	)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	sources: Mapped[list | None] = mapped_column(JSONB, nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	conversation: Mapped["Conversation"] = relationship(back_populates="messages")
	tool_calls: Mapped[list["AgentToolCall"]] = relationship(
		back_populates="message",
		cascade="all, delete",
	)


class AgentToolCall(Base):
	__tablename__ = "agent_tool_calls"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	message_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("messages.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	tool_name: Mapped[str] = mapped_column(
		SAEnum(
			"web_search",
			"fetch_news_by_category",
			"fetch_trending",
			"fact_check_search",
			"summarize_article",
			name="agent_tool",
		),
		nullable=False,
	)
	input_params: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
	output_result: Mapped[str | None] = mapped_column(Text, nullable=True)
	duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
	is_success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
	error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	message: Mapped["Message"] = relationship(back_populates="tool_calls")
