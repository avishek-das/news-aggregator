import pytest
from pathlib import Path
from app.adapters.rss_parser import parse_rss_feed

FIXTURES = Path(__file__).parent.parent / "fixtures"


def read(name: str) -> str:
    return (FIXTURES / name).read_text()


class TestRSS2:
    def test_returns_correct_count(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert len(items) == 3

    def test_extracts_title(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert items[0].title == "First RSS Item"

    def test_extracts_link(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert items[0].url == "https://example.com/item-1"

    def test_extracts_description(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert "first item" in items[0].excerpt

    def test_parses_pubdate(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert items[0].published_at is not None
        assert items[0].published_at.year == 2026

    def test_missing_date_returns_none(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "research")
        assert items[2].published_at is None

    def test_category_set_correctly(self):
        items = parse_rss_feed(read("rss_feed_sample.xml"), "community")
        assert all(i.category == "community" for i in items)

    def test_truncates_excerpt_to_500_chars(self):
        long_desc = "x" * 600
        xml = f"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <item><title>T</title><link>https://a.com</link><description>{long_desc}</description></item>
</channel></rss>"""
        items = parse_rss_feed(xml, "research")
        assert len(items[0].excerpt) <= 500


class TestAtom:
    def test_returns_correct_count(self):
        items = parse_rss_feed(read("atom_feed_sample.xml"), "research")
        assert len(items) == 2

    def test_extracts_title(self):
        items = parse_rss_feed(read("atom_feed_sample.xml"), "research")
        assert items[0].title == "First Atom Entry"

    def test_extracts_url_from_link_href(self):
        items = parse_rss_feed(read("atom_feed_sample.xml"), "research")
        assert items[0].url == "https://example.com/entry-1"

    def test_extracts_summary(self):
        items = parse_rss_feed(read("atom_feed_sample.xml"), "research")
        assert "first atom entry" in items[0].excerpt

    def test_parses_published(self):
        items = parse_rss_feed(read("atom_feed_sample.xml"), "research")
        assert items[0].published_at is not None
        assert items[0].published_at.year == 2026
