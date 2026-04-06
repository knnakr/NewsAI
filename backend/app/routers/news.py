from typing import Literal
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.news import ArticleCache, SavedArticle
from app.models.user import User
from app.schemas.news import ArticleResponse, SaveArticleRequest, SavedArticleResponse
from app.services.news_service import get_or_fetch_articles, get_trending_articles
from app.utils.cache import build_cache_key, get_cached_articles, set_cached_articles


router = APIRouter(prefix="/news", tags=["news"])


@router.get(
	"/feed",
	response_model=list[ArticleResponse],
	status_code=status.HTTP_200_OK,
	summary="Get news feed",
	description="Kategorize edilmiş haber feed'ini cache kullanarak döndürür.",
)
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


@router.get(
	"/category/{category}",
	response_model=list[ArticleResponse],
	status_code=status.HTTP_200_OK,
	summary="Get category news",
	description="Belirli bir kategori için haberleri ve alt filtreleri döndürür.",
)
async def get_category_news(
	category: Literal[
		"world",
		"technology",
		"sports",
		"economy",
		"health",
		"science",
		"entertainment",
	],
	subcategory: str | None = Query(default=None),
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=20, ge=1, le=50),
	db: AsyncSession = Depends(get_db),
):
	articles = await get_or_fetch_articles(category)

	if subcategory:
		needle = subcategory.lower()
		articles = [
			article
			for article in articles
			if needle in (article.get("title") or "").lower()
			or needle in (article.get("source_name") or "").lower()
			or needle in (article.get("url") or "").lower()
		]

	offset = (page - 1) * page_size
	return articles[offset : offset + page_size]


@router.get(
	"/trending",
	response_model=list[ArticleResponse],
	status_code=status.HTTP_200_OK,
	summary="Get trending news",
	description="Trend olan haberleri cache sıralamasına göre döndürür.",
)
async def get_trending(
	topic: Literal[
		"world",
		"technology",
		"sports",
		"economy",
		"health",
		"science",
		"entertainment",
	] | None = Query(default=None),
	db: AsyncSession = Depends(get_db),
):
	category = topic or "world"
	cache_key = build_cache_key(category, "trending")
	cached_articles = await get_cached_articles(cache_key, db, increment_view_count=True)

	if cached_articles is None:
		articles = await get_trending_articles(topic)
		await set_cached_articles(cache_key, articles, category, db)

	filters = [
		ArticleCache.expires_at > datetime.now(timezone.utc),
		ArticleCache.cache_key.like("%:trending"),
	]
	if topic is not None:
		filters.append(ArticleCache.category == topic)

	result = await db.execute(
		select(ArticleCache)
		.where(*filters)
		.order_by(ArticleCache.view_count.desc(), ArticleCache.updated_at.desc())
	)
	cache_entries = list(result.scalars().all())

	if not cache_entries:
		return cached_articles or []

	trending_articles: list[dict] = []
	for entry in cache_entries:
		trending_articles.extend(entry.articles_json)
	return trending_articles


@router.get(
	"/saved",
	response_model=list[SavedArticleResponse],
	status_code=status.HTTP_200_OK,
	summary="List saved articles",
	description="Giriş yapmış kullanıcının kaydettiği haberleri listeler.",
)
async def get_saved_articles(
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	result = await db.execute(
		select(SavedArticle)
		.where(SavedArticle.user_id == current_user.id)
		.order_by(SavedArticle.saved_at.desc())
	)
	articles = result.scalars().all()
	return [
		{
			"id": article.id,
			"title": article.title,
			"url": article.article_url,
			"source_name": article.source_name,
			"published_at": article.published_at.isoformat() if article.published_at else None,
			"ai_summary": article.ai_summary,
			"category": article.category,
			"saved_at": article.saved_at,
		}
		for article in articles
	]


@router.post(
	"/saved",
	response_model=SavedArticleResponse,
	status_code=status.HTTP_201_CREATED,
	summary="Save article",
	description="Bir haberi kullanıcının kayıtlı makalelerine ekler.",
)
async def save_article(
	body: SaveArticleRequest,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	article = SavedArticle(
		user_id=current_user.id,
		title=body.title,
		article_url=body.url,
		source_name=body.source_name,
		published_at=body.published_at,
		category=body.category,
	)
	db.add(article)
	try:
		await db.commit()
	except IntegrityError:
		await db.rollback()
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Bu makale zaten kaydedilmis",
		)

	await db.refresh(article)
	return {
		"id": article.id,
		"title": article.title,
		"url": article.article_url,
		"source_name": article.source_name,
		"published_at": article.published_at.isoformat() if article.published_at else None,
		"ai_summary": article.ai_summary,
		"category": article.category,
		"saved_at": article.saved_at,
	}


@router.delete(
	"/saved/{article_id}",
	status_code=status.HTTP_204_NO_CONTENT,
	summary="Delete saved article",
	description="Kaydedilmiş bir haberi kullanıcının listesinden siler.",
)
async def delete_saved_article(
	article_id: str,
	current_user: User = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	result = await db.execute(
		select(SavedArticle).where(
			SavedArticle.id == article_id,
			SavedArticle.user_id == current_user.id,
		)
	)
	article = result.scalar_one_or_none()
	if article is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kayit bulunamadi")

	await db.delete(article)
	await db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)
