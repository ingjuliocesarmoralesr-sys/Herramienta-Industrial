from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser
import httpx

from .config import settings


def viral_score(engagement: float, recency_hours: float) -> float:
    freshness_factor = max(0.2, 48 / (recency_hours + 2))
    return round((engagement ** 0.5) * freshness_factor, 2)


async def fetch_reddit(keyword: str) -> list[dict[str, Any]]:
    url = "https://www.reddit.com/search.json"
    headers = {"User-Agent": settings.reddit_user_agent}
    params = {"q": keyword, "sort": "top", "limit": 12, "t": "day"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()

    children = response.json().get("data", {}).get("children", [])
    results: list[dict[str, Any]] = []
    for child in children:
        data = child.get("data", {})
        created = datetime.fromtimestamp(data.get("created_utc", 0), tz=timezone.utc)
        hours_old = max((datetime.now(timezone.utc) - created).total_seconds() / 3600, 0.1)
        engagement = float(data.get("score", 0) + data.get("num_comments", 0) * 2)
        results.append(
            {
                "title": data.get("title", "Untitled Reddit Post"),
                "source": "Reddit",
                "keyword": keyword,
                "url": f"https://reddit.com{data.get('permalink', '')}",
                "engagement": engagement,
                "recency_hours": round(hours_old, 2),
            }
        )
    return results


async def fetch_youtube(keyword: str) -> list[dict[str, Any]]:
    if not settings.youtube_api_key:
        return []

    async with httpx.AsyncClient(timeout=20.0) as client:
        search = await client.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": keyword,
                "maxResults": 10,
                "order": "viewCount",
                "type": "video",
                "key": settings.youtube_api_key,
            },
        )
        search.raise_for_status()
        items = search.json().get("items", [])
        ids = [item.get("id", {}).get("videoId") for item in items if item.get("id", {}).get("videoId")]

        if not ids:
            return []

        stats = await client.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "statistics,snippet",
                "id": ",".join(ids),
                "key": settings.youtube_api_key,
            },
        )
        stats.raise_for_status()

    results: list[dict[str, Any]] = []
    for item in stats.json().get("items", []):
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        published_at = datetime.fromisoformat(snippet.get("publishedAt", "1970-01-01T00:00:00+00:00").replace("Z", "+00:00"))
        hours_old = max((datetime.now(timezone.utc) - published_at).total_seconds() / 3600, 0.1)
        views = float(statistics.get("viewCount", 0))
        comments = float(statistics.get("commentCount", 0))
        likes = float(statistics.get("likeCount", 0))
        engagement = views + (likes * 6) + (comments * 10)
        results.append(
            {
                "title": snippet.get("title", "Untitled YouTube Video"),
                "source": "YouTube",
                "keyword": keyword,
                "url": f"https://www.youtube.com/watch?v={item.get('id')}",
                "engagement": engagement,
                "recency_hours": round(hours_old, 2),
            }
        )
    return results


async def fetch_google_news(keyword: str) -> list[dict[str, Any]]:
    rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    results: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc)

    for entry in feed.entries[:15]:
        published = entry.get("published")
        published_dt = parsedate_to_datetime(published) if published else now
        if published_dt.tzinfo is None:
            published_dt = published_dt.replace(tzinfo=timezone.utc)
        hours_old = max((now - published_dt).total_seconds() / 3600, 0.1)
        title = entry.get("title", "Untitled Article")
        engagement_proxy = float(max(5, 100 - min(hours_old, 72)) + len(title) / 4)
        results.append(
            {
                "title": title,
                "source": "Google News",
                "keyword": keyword,
                "url": entry.get("link", "https://news.google.com"),
                "engagement": engagement_proxy,
                "recency_hours": round(hours_old, 2),
            }
        )
    return results


async def collect_trends(keyword: str) -> list[dict[str, Any]]:
    reddit = await fetch_reddit(keyword)
    youtube = await fetch_youtube(keyword)
    news = await fetch_google_news(keyword)
    combined = reddit + youtube + news

    for item in combined:
        item["viral_score"] = viral_score(item["engagement"], item["recency_hours"])

    combined.sort(key=lambda x: x["viral_score"], reverse=True)
    return combined
