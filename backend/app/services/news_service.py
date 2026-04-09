from __future__ import annotations

import xml.etree.ElementTree as ET

import httpx

from app.config import settings


NEWSAPI_CATEGORY_MAP: dict[str, dict[str, str]] = {
	"world": {"q": "world news"},
	"technology": {"category": "technology"},
	"sports": {"category": "sports"},
	"economy": {"q": "economy news"},
	"health": {"category": "health"},
	"science": {"category": "science"},
	"entertainment": {"category": "entertainment"},
}


def _normalize_article(
	*,
	title: str,
	url: str,
	source_name: str,
	published_at: str | None,
	category: str,
) -> dict:
	return {
		"title": title,
		"url": url,
		"source_name": source_name,
		"published_at": published_at,
		"ai_summary": None,
		"category": category,
	}


async def fetch_from_newsapi(category: str, from_date: str | None = None) -> list[dict]:
	"""Fetch articles from NewsAPI's top headlines endpoint."""
	params: dict[str, str | int] = {
		"apiKey": settings.NEWS_API_KEY,
		"pageSize": 20,
	}
	params.update(NEWSAPI_CATEGORY_MAP.get(category, {"category": category}))
	if from_date:
		params["from"] = from_date

	async with httpx.AsyncClient(timeout=10.0) as client:
		response = await client.get("https://newsapi.org/v2/top-headlines", params=params)
		response.raise_for_status()
		articles = response.json().get("articles", [])

	normalized_articles: list[dict] = []
	for article in articles:
		url = article.get("url")
		if not url:
			continue

		source = article.get("source") or {}
		normalized_articles.append(
			_normalize_article(
				title=article.get("title") or "",
				url=url,
				source_name=source.get("name") or "NewsAPI",
				published_at=article.get("publishedAt"),
				category=category,
			)
		)

	return normalized_articles


async def fetch_from_rss(category: str, query: str | None = None) -> list[dict]:
	"""Fetch articles from Google News RSS as a fallback."""
	rss_query = query or category
	rss_url = f"https://news.google.com/rss/search?q={rss_query}&hl=tr&gl=TR&ceid=TR:tr"

	async with httpx.AsyncClient(timeout=10.0) as client:
		response = await client.get(rss_url)
		response.raise_for_status()

	root = ET.fromstring(response.text)
	normalized_articles: list[dict] = []

	for item in root.findall(".//item"):
		url = item.findtext("link")
		if not url:
			continue

		normalized_articles.append(
			_normalize_article(
				title=item.findtext("title", "") or "",
				url=url,
				source_name="Google News",
				published_at=item.findtext("pubDate"),
				category=category,
			)
		)

	return normalized_articles


async def get_or_fetch_articles(category: str, from_date: str | None = None) -> list[dict]:
	"""Fetch NewsAPI articles first, then fall back to RSS if needed."""
	try:
		articles = await fetch_from_newsapi(category, from_date=from_date)
		if articles:
			return articles
	except Exception:
		articles = []

	if category == "world":
		return await fetch_from_rss(category, query="world news")
	if category == "economy":
		return await fetch_from_rss(category, query="economy news")

	return articles or await fetch_from_rss(category)


async def get_trending_articles(topic: str | None = None) -> list[dict]:
	"""Return trending articles using the same fetch/fallback flow."""
	category = topic or "world"
	return await get_or_fetch_articles(category)
