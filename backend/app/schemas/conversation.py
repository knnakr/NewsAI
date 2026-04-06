from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
	title: str | None = None

	model_config = ConfigDict(
		json_schema_extra={"example": {"title": "Morning news"}}
	)


class ConversationUpdate(BaseModel):
	title: str = Field(min_length=1, max_length=200)

	model_config = ConfigDict(
		json_schema_extra={"example": {"title": "Updated title"}}
	)


class ConversationResponse(BaseModel):
	id: uuid.UUID
	title: str | None
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": "22222222-2222-2222-2222-222222222222",
				"title": "Morning news",
				"created_at": "2026-04-05T12:00:00Z",
				"updated_at": "2026-04-05T12:00:00Z",
			}
		},
	)


class MessageCreate(BaseModel):
	content: str = Field(min_length=1, max_length=4000)

	model_config = ConfigDict(
		json_schema_extra={"example": {"content": "What is trending today?"}}
	)


class MessageResponse(BaseModel):
	id: uuid.UUID
	role: str
	content: str
	sources: list[dict] | None
	created_at: datetime

	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": "33333333-3333-3333-3333-333333333333",
				"role": "assistant",
				"content": "Here is the latest update.",
				"sources": [{"url": "https://example.com"}],
				"created_at": "2026-04-05T12:00:00Z",
			}
		},
	)


class ConversationDetailResponse(ConversationResponse):
	messages: list[MessageResponse]

	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": "22222222-2222-2222-2222-222222222222",
				"title": "Morning news",
				"created_at": "2026-04-05T12:00:00Z",
				"updated_at": "2026-04-05T12:00:00Z",
				"messages": [],
			}
		},
	)
