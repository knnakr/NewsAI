from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
	title: str | None = None


class ConversationUpdate(BaseModel):
	title: str = Field(min_length=1, max_length=200)


class ConversationResponse(BaseModel):
	id: uuid.UUID
	title: str | None
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
	content: str = Field(min_length=1, max_length=4000)


class MessageResponse(BaseModel):
	id: uuid.UUID
	role: str
	content: str
	sources: list[dict] | None
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)


class ConversationDetailResponse(ConversationResponse):
	messages: list[MessageResponse]
