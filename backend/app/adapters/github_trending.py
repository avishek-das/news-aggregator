import logging
from html.parser import HTMLParser
import httpx
from app.adapters.base import RawItem, SourceAdapter

logger = logging.getLogger(__name__)
GITHUB_TRENDING = "https://github.com/trending/{language}?since=daily"


class _TrendingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.repos: list[dict] = []
        self._in_article = False
        self._in_h2 = False
        self._in_link = False
        self._in_desc = False
        self._current: dict = {}
        self._depth = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attr_dict = dict(attrs)
        if tag == "article" and "Box-row" in attr_dict.get("class", ""):
            self._in_article = True
            self._current = {}
        if not self._in_article:
            return
        if tag == "h2" and self._in_article:
            self._in_h2 = True
        if self._in_h2 and tag == "a":
            href = attr_dict.get("href", "").strip("/")
            if href.count("/") == 1:
                self._current["path"] = href
                self._in_link = True
        if tag == "p" and "color-fg-muted" in attr_dict.get("class", ""):
            self._in_desc = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "article" and self._in_article:
            if self._current.get("path"):
                self.repos.append(dict(self._current))
            self._in_article = False
            self._in_h2 = False
        if tag == "h2":
            self._in_h2 = False
            self._in_link = False
        if tag == "p" and self._in_desc:
            self._in_desc = False

    def handle_data(self, data: str) -> None:
        if self._in_desc and self._in_article:
            self._current.setdefault("description", "")
            self._current["description"] += data.strip()


class GitHubTrendingAdapter(SourceAdapter):
    def _parse(self, html: str, language: str) -> list[RawItem]:
        parser = _TrendingParser()
        try:
            parser.feed(html)
        except Exception as exc:
            logger.warning("GitHub Trending HTML parse error: %s", exc)
            return []

        items: list[RawItem] = []
        for repo in parser.repos:
            path = repo.get("path", "")
            if not path or "/" not in path:
                continue
            url = f"https://github.com/{path}"
            title = path  # "owner/repo" format
            excerpt = repo.get("description", "").strip()
            items.append(RawItem(
                title=title,
                url=url,
                excerpt=excerpt,
                published_at=None,
                category="code",
                raw_metadata={"language": language},
            ))
        return items

    async def fetch(self) -> list[RawItem]:
        language = self.fetch_config.get("language", "python")
        url = self.fetch_config.get("url", GITHUB_TRENDING.format(language=language))
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers={"User-Agent": "news-aggregator/1.0"},
                follow_redirects=True,
            )
            response.raise_for_status()
            return self._parse(response.text, language)
