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


@pytest.fixture
async def auth_headers(client) -> dict[str, str]:
	await client.post(
		"/auth/register",
		json={
			"email": "saved-news-user1@example.com",
			"password": "password123",
			"display_name": "Saved News User One",
		},
	)
	login_response = await client.post(
		"/auth/login",
		json={
			"email": "saved-news-user1@example.com",
			"password": "password123",
		},
	)
	token = login_response.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def auth_headers_user2(client) -> dict[str, str]:
	await client.post(
		"/auth/register",
		json={
			"email": "saved-news-user2@example.com",
			"password": "password123",
			"display_name": "Saved News User Two",
		},
	)
	login_response = await client.post(
		"/auth/login",
		json={
			"email": "saved-news-user2@example.com",
			"password": "password123",
		},
	)
	token = login_response.json()["access_token"]
	return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_newsapi(monkeypatch):
	call_count = {"count": 0}

	async def fake_get_or_fetch_articles(category, from_date=None):
		call_count["count"] += 1
		return [
			{
				"title": f"Trending {category}",
				"url": f"http://trending-{category}.com",
				"source_name": "Trending Source",
				"published_at": None,
				"ai_summary": None,
				"category": category,
			},
		]

	monkeypatch.setattr("app.routers.news.get_or_fetch_articles", fake_get_or_fetch_articles)
	return call_count


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


async def test_summarize_article_returns_cached_summary(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return [
			{
				"title": "Cached",
				"url": "https://example.com/a",
				"source_name": "Example",
				"published_at": None,
				"ai_summary": "Cached summary",
				"category": "technology",
			}
		]

	mock_summary = AsyncMock(return_value="Should not run")
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/a",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 200
	assert response.json()["cached"] is True
	assert response.json()["ai_summary"] == "Cached summary"
	mock_summary.assert_not_called()


async def test_summarize_article_generates_and_stores_summary(client, monkeypatch):
	set_cache_calls = {"count": 0}

	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return None

	async def fake_set_cached_articles(cache_key, articles, category, db):
		set_cache_calls["count"] += 1
		assert articles[0]["ai_summary"] == "Generated summary"

	mock_summary = AsyncMock(return_value="Generated summary")
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.set_cached_articles", fake_set_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/new",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 200
	assert response.json()["cached"] is False
	assert response.json()["ai_summary"] == "Generated summary"
	assert set_cache_calls["count"] == 1
	mock_summary.assert_awaited_once()


async def test_summarize_article_rate_limit_maps_to_429(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return None

	mock_summary = AsyncMock(side_effect=Exception("RateLimitError: rate limit reached"))
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/rate",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 429
	assert response.json()["detail"]["error_type"] == "rate_limit"


async def test_summarize_article_too_many_requests_maps_to_429(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return None

	mock_summary = AsyncMock(side_effect=Exception("Too many requests from provider"))
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/tmr",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 429
	assert response.json()["detail"]["error_type"] == "too_many_requests"


async def test_summarize_article_timeout_maps_to_504(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return None

	mock_summary = AsyncMock(side_effect=Exception("ReadTimeout: request timed out"))
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/timeout",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 504
	assert response.json()["detail"]["error_type"] == "timeout"


async def test_summarize_article_unknown_error_maps_to_502(client, monkeypatch):
	async def fake_get_cached_articles(cache_key, db, increment_view_count=False):
		return None

	mock_summary = AsyncMock(side_effect=Exception("Unexpected provider crash"))
	monkeypatch.setattr("app.routers.news.get_cached_articles", fake_get_cached_articles)
	monkeypatch.setattr("app.routers.news.run_article_summary_crew", mock_summary)

	response = await client.post(
		"/news/summarize",
		json={
			"title": "Some article",
			"url": "https://example.com/gateway",
			"source_name": "Example",
			"published_at": None,
			"category": "technology",
		},
	)

	assert response.status_code == 502
	assert response.json()["detail"]["error_type"] == "bad_gateway"


async def test_get_trending_returns_article_list(client, mock_newsapi):
	response = await client.get("/news/trending")

	assert response.status_code == 200
	assert isinstance(response.json(), list)


async def test_get_trending_with_topic_filter(client, mock_newsapi):
	response = await client.get("/news/trending?topic=technology")

	assert response.status_code == 200


async def test_view_count_increments_on_trending_cache_hit(db, client, mock_newsapi):
	await client.get("/news/trending")
	await client.get("/news/trending")

	result = await db.execute(text("SELECT MAX(view_count) FROM article_cache"))
	count = result.scalar() or 0
	assert count >= 1


async def test_get_category_news_returns_article_list(client, mock_newsapi):
	response = await client.get("/news/category/technology")

	assert response.status_code == 200
	assert isinstance(response.json(), list)


async def test_get_category_news_invalid_category_returns_422(client):
	response = await client.get("/news/category/invalid_xyz")

	assert response.status_code == 422


async def test_get_category_news_with_subcategory_filter(client, mock_newsapi):
	response = await client.get("/news/category/sports?subcategory=football")

	assert response.status_code == 200


async def test_get_category_news_pagination(client, mock_newsapi):
	response = await client.get("/news/category/technology?page=1&page_size=5")

	assert response.status_code == 200
	assert len(response.json()) <= 5


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


async def test_save_article_returns_201(client, auth_headers):
	response = await client.post(
		"/news/saved",
		json={
			"title": "Test Article",
			"url": "http://test.com/article",
			"source_name": "Test Source",
			"published_at": "2026-04-05T12:00:00Z",
			"category": "technology",
		},
		headers=auth_headers,
	)

	assert response.status_code == 201
	assert "id" in response.json()
	assert response.json()["published_at"] is not None


async def test_save_same_article_twice_returns_409(client, auth_headers):
	article = {
		"title": "Dup",
		"url": "http://dup.com",
		"source_name": "Src",
		"category": "technology",
	}

	first_response = await client.post("/news/saved", json=article, headers=auth_headers)
	second_response = await client.post("/news/saved", json=article, headers=auth_headers)

	assert first_response.status_code == 201
	assert second_response.status_code == 409


async def test_get_saved_articles_returns_only_current_user(client, auth_headers, auth_headers_user2):
	await client.post(
		"/news/saved",
		json={
			"title": "A1",
			"url": "http://a1.com",
			"source_name": "S",
			"category": "technology",
		},
		headers=auth_headers,
	)
	await client.post(
		"/news/saved",
		json={
			"title": "A2",
			"url": "http://a2.com",
			"source_name": "S",
			"category": "technology",
		},
		headers=auth_headers_user2,
	)

	response = await client.get("/news/saved", headers=auth_headers)

	assert response.status_code == 200
	assert len(response.json()) == 1
	assert response.json()[0]["title"] == "A1"


async def test_delete_saved_article_removes_from_db(client, auth_headers):
	create_response = await client.post(
		"/news/saved",
		json={
			"title": "Del",
			"url": "http://del.com",
			"source_name": "S",
			"category": "technology",
		},
		headers=auth_headers,
	)
	article_id = create_response.json()["id"]

	delete_response = await client.delete(f"/news/saved/{article_id}", headers=auth_headers)
	list_response = await client.get("/news/saved", headers=auth_headers)

	assert delete_response.status_code == 204
	assert list_response.status_code == 200
	assert len(list_response.json()) == 0


async def test_save_article_requires_auth(client):
	response = await client.post(
		"/news/saved",
		json={
			"title": "T",
			"url": "http://t.com",
			"source_name": "S",
			"category": "technology",
		},
	)

	assert response.status_code == 401


async def test_save_article_invalid_body_returns_422(client, auth_headers):
	response = await client.post(
		"/news/saved",
		json={
			"title": "T",
			"source_name": "S",
			"category": "technology",
		},
		headers=auth_headers,
	)

	assert response.status_code == 422
