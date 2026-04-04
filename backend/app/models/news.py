import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.user import Base

if TYPE_CHECKING:
    from app.models.user import User


class SavedArticle(Base):
	__tablename__ = "saved_articles"
	__table_args__ = (
		UniqueConstraint("user_id", "article_url", name="uq_saved_articles_user_article_url"),
	)

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		index=True,
	)
	title: Mapped[str] = mapped_column(Text, nullable=False)
	article_url: Mapped[str] = mapped_column(Text, nullable=False)
	source_name: Mapped[str] = mapped_column(String(255), nullable=False)
	published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	category: Mapped[str] = mapped_column(
		SAEnum(
			"world",
			"technology",
			"sports",
			"economy",
			"health",
			"science",
			"entertainment",
			name="news_category",
		),
		nullable=False,
	)
	ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
	saved_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		nullable=False,
		server_default=func.now(),
	)

	user: Mapped["User"] = relationship(back_populates="saved_articles")


class ArticleCache(Base):
    __tablename__ = "article_cache"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(
        SAEnum(
            "world",
            "technology",
            "sports",
            "economy",
            "health",
            "science",
            "entertainment",
            name="news_category",
        ),
        nullable=False,
    )
    articles_json: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
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
