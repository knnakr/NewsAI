from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import text

from app.crew.tools.fetch_news import FetchNewsTool
from app.crew.tools.fetch_trending import FetchTrendingTool
from app.main import shutdown_event, startup_event
from app.services.news_service import fetch_from_newsapi, fetch_from_rss, get_or_fetch_articles
from app.utils.cache import build_cache_key, get_cached_articles, run_cleanup, set_cached_articles


def _mock_async_client(response: MagicMock):
	client = AsyncMock()
	client.get = AsyncMock(return_value=response)
	async_client = MagicMock()
	async_client.__aenter__ = AsyncMock(return_value=client)
	async_client.__aexit__ = AsyncMock(return_value=None)
	return client, async_client


async def test_fetch_from_newsapi_returns_article_list():
	response = MagicMock()
	response.raise_for_status = MagicMock()
	response.json.return_value = {
		"articles": [
			{
				"title": "Test Article",
				"url": "http://test.com",
				"source": {"name": "Test Source"},
				"publishedAt": "2024-01-01T00:00:00Z",
			}
		]
	}

	_, async_client = _mock_async_client(response)

	with patch("app.services.news_service.httpx.AsyncClient", return_value=async_client):
		result = await fetch_from_newsapi("technology")

	assert isinstance(result, list)
	assert len(result) == 1
	assert result[0]["title"] == "Test Article"
	assert result[0]["url"] == "http://test.com"
	assert result[0]["source_name"] == "Test Source"
	assert result[0]["published_at"] == "2024-01-01T00:00:00Z"
	assert result[0]["category"] == "technology"
	assert result[0]["ai_summary"] is None


async def test_fetch_from_newsapi_excludes_articles_without_url():
	response = MagicMock()
	response.raise_for_status = MagicMock()
	response.json.return_value = {
		"articles": [
			{
				"title": "No URL",
				"url": None,
				"source": {"name": "Source"},
				"publishedAt": "2024-01-01",
			},
			{
				"title": "Has URL",
				"url": "http://has.com",
				"source": {"name": "Source"},
				"publishedAt": "2024-01-01",
			},
		]
	}

	_, async_client = _mock_async_client(response)

	with patch("app.services.news_service.httpx.AsyncClient", return_value=async_client):
		result = await fetch_from_newsapi("technology")

	assert len(result) == 1
	assert result[0]["title"] == "Has URL"


async def test_fetch_from_newsapi_raises_on_http_error():
	response = MagicMock()
	response.raise_for_status = MagicMock(side_effect=Exception("HTTP Error"))

	_, async_client = _mock_async_client(response)

	with patch("app.services.news_service.httpx.AsyncClient", return_value=async_client):
		with pytest.raises(Exception, match="HTTP Error"):
			await fetch_from_newsapi("technology")


async def test_rss_fallback_returns_list():
	response = MagicMock()
	response.text = (
		'<?xml version="1.0"?><rss><channel>'
		'<item><title>RSS Article</title><link>http://rss.com</link><pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate></item>'
		'</channel></rss>'
	)

	_, async_client = _mock_async_client(response)

	with patch("app.services.news_service.httpx.AsyncClient", return_value=async_client):
		result = await fetch_from_rss("technology")

	assert isinstance(result, list)
	assert len(result) == 1
	assert result[0]["title"] == "RSS Article"
	assert result[0]["url"] == "http://rss.com"
	assert result[0]["source_name"] == "Google News"


async def test_get_or_fetch_articles_falls_back_to_rss_when_newsapi_fails():
	with patch("app.services.news_service.fetch_from_newsapi", side_effect=Exception("NewsAPI down")) as mock_newsapi:
		with patch(
			"app.services.news_service.fetch_from_rss",
			return_value=[{"title": "RSS Article", "url": "http://rss.com", "source_name": "Google News", "published_at": None, "ai_summary": None, "category": "technology"}],
		) as mock_rss:
			result = await get_or_fetch_articles("technology")

	mock_newsapi.assert_called_once_with("technology", from_date=None)
	mock_rss.assert_called_once_with("technology")
	assert result[0]["title"] == "RSS Article"


async def test_get_cached_articles_returns_none_when_no_cache(db):
	result = await get_cached_articles("technology:default", db)
	assert result is None


async def test_set_and_get_cached_articles(db):
	articles = [{"title": "Test", "url": "http://test.com", "source_name": "Source", "published_at": None, "ai_summary": None, "category": "technology"}]
	await set_cached_articles("technology:default", articles, "technology", db)
	result = await get_cached_articles("technology:default", db)
	assert result == articles


async def test_get_cached_articles_returns_none_when_expired(db):
	articles = [{"title": "Old", "url": "http://old.com", "source_name": "Source", "published_at": None, "ai_summary": None, "category": "technology"}]
	await set_cached_articles("tech:expired", articles, "technology", db)
	await db.execute(text("UPDATE article_cache SET expires_at = NOW() - INTERVAL '1 hour' WHERE cache_key = 'tech:expired'"))
	await db.commit()
	result = await get_cached_articles("tech:expired", db)
	assert result is None


async def test_request_count_increments_on_cache_hit(db):
	articles = [{"title": "Hit", "url": "http://hit.com", "source_name": "Source", "published_at": None, "ai_summary": None, "category": "technology"}]
	await set_cached_articles("tech:hit", articles, "technology", db)
	await get_cached_articles("tech:hit", db)
	await get_cached_articles("tech:hit", db)
	result = await db.execute(text("SELECT request_count FROM article_cache WHERE cache_key = 'tech:hit'"))
	count = result.scalar()
	assert count == 2


def test_build_cache_key_format():
	assert build_cache_key("technology", "today") == "technology:today"


async def test_get_news_feed_returns_article_list(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db):
		return None

	async def fake_get_or_fetch_articles(category, from_date=None):
		return [
			{
				"title": "Feed Article",
				"url": "http://feed.com",
				"source_name": "Feed Source",
				"published_at": "2024-01-01T00:00:00Z",
				"ai_summary": None,
				"category": category,
			},
		]

	async def fake_set_cached_articles(cache_key, articles, category, db):
		return None

	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)
	monkeypatch.setattr("app.routers.news.set_cached_articles", fake_set_cached_articles)

	response = await client.get("/news/feed?category=technology")

	assert response.status_code == 200
	assert isinstance(response.json(), list)
	assert response.json()[0]["title"] == "Feed Article"


async def test_get_news_feed_invalid_category_returns_422(client):
	response = await client.get("/news/feed?category=invalid_category_xyz")

	assert response.status_code == 422


async def test_get_news_feed_uses_cache_on_second_request(client, monkeypatch):
	cache: dict[str, list[dict] | None] = {}
	fetch_calls = {"count": 0}

	async def fake_get_cached_articles(cache_key, db):
		return cache.get(cache_key)

	async def fake_get_or_fetch_articles(category, from_date=None):
		fetch_calls["count"] += 1
		return [
			{
				"title": "Cached Feed Article",
				"url": "http://cached-feed.com",
				"source_name": "Feed Source",
				"published_at": None,
				"ai_summary": None,
				"category": category,
			},
		]

	async def fake_set_cached_articles(cache_key, articles, category, db):
		cache[cache_key] = articles

	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)
	monkeypatch.setattr("app.routers.news.set_cached_articles", fake_set_cached_articles)

	first_response = await client.get("/news/feed?category=technology")
	second_response = await client.get("/news/feed?category=technology")

	assert first_response.status_code == 200
	assert second_response.status_code == 200
	assert fetch_calls["count"] == 1
	assert second_response.json()[0]["title"] == "Cached Feed Article"


async def test_get_news_feed_does_not_require_auth(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db):
		return None

	async def fake_get_or_fetch_articles(category, from_date=None):
		return []

	async def fake_set_cached_articles(cache_key, articles, category, db):
		return None

	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)
	monkeypatch.setattr("app.routers.news.set_cached_articles", fake_set_cached_articles)

	response = await client.get("/news/feed?category=technology")

	assert response.status_code == 200


async def test_get_news_feed_response_has_required_fields(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db):
		return None

	async def fake_get_or_fetch_articles(category, from_date=None):
		return [
			{
				"title": "Schema Article",
				"url": "http://schema.com",
				"source_name": "Schema Source",
				"published_at": None,
				"ai_summary": None,
				"category": category,
			},
		]

	async def fake_set_cached_articles(cache_key, articles, category, db):
		return None

	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)
	monkeypatch.setattr("app.routers.news.set_cached_articles", fake_set_cached_articles)

	response = await client.get("/news/feed?category=technology")

	assert response.status_code == 200
	article = response.json()[0]
	assert "title" in article
	assert "url" in article
	assert "category" in article


async def test_run_cleanup_deletes_expired_cache_entries(db):
	await set_cached_articles("expired:key", [], "technology", db)
	await db.execute(text("UPDATE article_cache SET expires_at = NOW() - INTERVAL '1 hour' WHERE cache_key = 'expired:key'"))
	await db.commit()

	await run_cleanup(db)

	result = await db.execute(text("SELECT COUNT(*) FROM article_cache WHERE cache_key = 'expired:key'"))
	assert result.scalar() == 0


async def test_run_cleanup_keeps_valid_cache_entries(db):
	await set_cached_articles("valid:key", [], "technology", db)
	await db.commit()

	await run_cleanup(db)

	result = await db.execute(text("SELECT COUNT(*) FROM article_cache WHERE cache_key = 'valid:key'"))
	assert result.scalar() == 1


async def test_startup_event_schedules_cleanup_job(monkeypatch):
	mock_scheduler = MagicMock()
	monkeypatch.setattr("app.main.scheduler", mock_scheduler)

	await startup_event()

	mock_scheduler.add_job.assert_called_once()
	_, kwargs = mock_scheduler.add_job.call_args
	assert kwargs["trigger"] == "interval"
	assert kwargs["hours"] == 6
	mock_scheduler.start.assert_called_once_with()


async def test_shutdown_event_stops_scheduler(monkeypatch):
	mock_scheduler = MagicMock()
	monkeypatch.setattr("app.main.scheduler", mock_scheduler)

	await shutdown_event()

	mock_scheduler.shutdown.assert_called_once_with()


def test_fetch_news_tool_name_matches_enum():
	tool = FetchNewsTool()
	assert tool.name == "fetch_news_by_category"


def test_fetch_trending_tool_name_matches_enum():
	tool = FetchTrendingTool()
	assert tool.name == "fetch_trending"


async def test_fetch_news_tool_arun_returns_list(monkeypatch):
	async def fake_get_or_fetch_articles(category, from_date=None):
		return [{"title": "Test", "url": "http://test.com"}]

	monkeypatch.setattr("app.crew.tools.fetch_news.get_or_fetch_articles", fake_get_or_fetch_articles)

	tool = FetchNewsTool()
	result = await tool._arun(category="technology")

	assert isinstance(result, list)
	assert len(result) == 1


async def test_fetch_news_tool_accepts_valid_categories():
	tool = FetchNewsTool()

	with pytest.raises(Exception):
		await tool._arun(category="invalid_cat")
