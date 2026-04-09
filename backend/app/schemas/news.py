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

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"title": "Example article",
				"url": "https://example.com/article",
				"source_name": "Example Source",
				"published_at": "2026-04-05T12:00:00Z",
				"ai_summary": "Short summary.",
				"category": "technology",
			}
		}
	)


class SaveArticleRequest(BaseModel):
	title: str
	url: str
	source_name: str
	published_at: str | None = None
	category: str

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"title": "Example article",
				"url": "https://example.com/article",
				"source_name": "Example Source",
				"published_at": "2026-04-05T12:00:00Z",
				"category": "technology",
			}
		}
	)


class SavedArticleResponse(ArticleResponse):
	id: uuid.UUID
	saved_at: datetime
	model_config = ConfigDict(
		from_attributes=True,
		json_schema_extra={
			"example": {
				"id": "44444444-4444-4444-4444-444444444444",
				"title": "Example article",
				"url": "https://example.com/article",
				"source_name": "Example Source",
				"published_at": "2026-04-05T12:00:00Z",
				"ai_summary": "Short summary.",
				"category": "technology",
				"saved_at": "2026-04-05T12:00:00Z",
			}
		},
	)


class SummarizeArticleRequest(BaseModel):
	title: str
	url: str
	source_name: str
	published_at: str | None = None
	category: str

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"title": "Example article",
				"url": "https://example.com/article",
				"source_name": "Example Source",
				"published_at": "2026-04-05T12:00:00Z",
				"category": "technology",
			}
		}
	)


class SummarizeArticleResponse(BaseModel):
	url: str
	ai_summary: str
	cached: bool = False

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"url": "https://example.com/article",
				"ai_summary": "This article explains the latest AI chip launch and its market impact.",
				"cached": True,
			}
		}
	)
