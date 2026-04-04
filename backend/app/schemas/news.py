from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
	title: str
	url: str
	source_name: str
	published_at: str | None = None
	ai_summary: str | None = None
	category: str


class SaveArticleRequest(BaseModel):
	title: str
	url: str
	source_name: str
	published_at: str | None = None
	category: str


class SavedArticleResponse(ArticleResponse):
	id: uuid.UUID
	saved_at: datetime
	model_config = ConfigDict(from_attributes=True)
