from __future__ import annotations

from datetime import datetime, timezone, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.news import ArticleCache


def build_cache_key(category: str, period: str | None = None) -> str:
	return f"{category}:{period or 'default'}"


async def get_cached_articles(
	cache_key: str,
	db: AsyncSession,
	increment_view_count: bool = False,
) -> list[dict] | None:
	"""Return cached articles when the entry is still valid."""
	result = await db.execute(
		select(ArticleCache).where(
			ArticleCache.cache_key == cache_key,
			ArticleCache.expires_at > datetime.now(timezone.utc),
		)
	)
	entry = result.scalar_one_or_none()
	if not entry:
		return None
	if not entry.articles_json:
		return None

	entry.request_count += 1
	if increment_view_count:
		entry.view_count += 1
	await db.commit()
	return entry.articles_json


async def set_cached_articles(
	cache_key: str,
	articles: list[dict],
	category: str,
	db: AsyncSession,
) -> None:
	"""Store articles in cache and refresh the TTL."""
	expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.ARTICLE_CACHE_TTL_HOURS)

	result = await db.execute(select(ArticleCache).where(ArticleCache.cache_key == cache_key))
	entry = result.scalar_one_or_none()

	if entry:
		entry.articles_json = articles
		entry.category = category
		entry.expires_at = expires_at
	else:
		db.add(
			ArticleCache(
				cache_key=cache_key,
				category=category,
				articles_json=articles,
				expires_at=expires_at,
			)
		)

	await db.commit()


async def run_cleanup(db: AsyncSession) -> None:
	"""Remove expired cache rows."""
	await db.execute(text("DELETE FROM article_cache WHERE expires_at <= NOW()"))
	await db.commit()
