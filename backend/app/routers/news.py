from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.news import ArticleResponse, SaveArticleRequest, SavedArticleResponse
from app.services.news_service import get_or_fetch_articles
from app.utils.cache import build_cache_key, get_cached_articles, set_cached_articles


router = APIRouter(prefix="/news", tags=["news"])


@router.get("/feed", response_model=list[ArticleResponse])
async def get_news_feed(
	category: Literal[
		"world",
		"technology",
		"sports",
		"economy",
		"health",
		"science",
		"entertainment",
	] = Query(...),
	period: str | None = None,
	db: AsyncSession = Depends(get_db),
):
	cache_key = build_cache_key(category, period)
	cached_articles = await get_cached_articles(cache_key, db)
	if cached_articles is not None:
		return cached_articles

	articles = await get_or_fetch_articles(category)
	await set_cached_articles(cache_key, articles, category, db)
	return articles
