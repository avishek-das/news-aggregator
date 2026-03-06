import asyncio
from datetime import datetime, timezone
import httpx
from app.adapters.base import RawItem, SourceAdapter

REDDIT_JSON = "https://www.reddit.com/r/{subreddit}.json?limit=50&t=day"
USER_AGENT = "news-aggregator/1.0 (educational project)"


class RedditAdapter(SourceAdapter):
    def _parse(self, data: dict, min_score: int) -> list[RawItem]:
        items: list[RawItem] = []
        children = data.get("data", {}).get("children", [])
        for child in children:
            post = child.get("data", {})
            score = post.get("score", 0)
            if score < min_score:
                continue
            title = (post.get("title") or "").strip()
            is_self = post.get("is_self", False)
            permalink = post.get("permalink", "")
            external_url = post.get("url", "")
            url = (
                f"https://www.reddit.com{permalink}"
                if is_self or not external_url
                else external_url
            )
            selftext = (post.get("selftext") or "").strip()[:500]
            created_utc = post.get("created_utc")
            pub: datetime | None = None
            if created_utc:
                pub = datetime.fromtimestamp(created_utc, tz=timezone.utc)

            if title and url:
                items.append(RawItem(
                    title=title,
                    url=url,
                    excerpt=selftext,
                    published_at=pub,
                    category="community",
                    raw_metadata={
                        "score": score,
                        "num_comments": post.get("num_comments", 0),
                        "subreddit": post.get("subreddit", ""),
                    },
                ))
        return items

    async def fetch(self) -> list[RawItem]:
        subreddits: list[str] = self.fetch_config.get("subreddits", [])
        min_score: int = self.fetch_config.get("min_score", 10)
        all_items: list[RawItem] = []
        headers = {"User-Agent": USER_AGENT}
        async with httpx.AsyncClient(timeout=30, headers=headers) as client:
            for i, sub in enumerate(subreddits):
                if i > 0:
                    await asyncio.sleep(1)  # Reddit rate limiting
                url = REDDIT_JSON.format(subreddit=sub)
                response = await client.get(url)
                response.raise_for_status()
                all_items.extend(self._parse(response.json(), min_score))
        return all_items
