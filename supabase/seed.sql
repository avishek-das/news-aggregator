-- Seed: 3 test sources for Phase 1.1 development
-- Run after migration 001. Safe to run multiple times (ON CONFLICT DO NOTHING).

INSERT INTO sources (name, url, type, category, priority, status, fetch_config)
VALUES
  (
    'arXiv cs.AI',
    'https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&max_results=50',
    'api', 'research', 'high', 'active',
    '{"adapter": "arxiv", "categories": ["cs.AI"]}'
  ),
  (
    'Hacker News',
    'https://hn.algolia.com/api/v1/search?tags=story&query=AI&hitsPerPage=50',
    'api', 'community', 'high', 'active',
    '{"adapter": "hackernews", "min_score": 10}'
  ),
  (
    'GitHub Trending',
    'https://github.com/trending/python?since=daily',
    'scrape', 'code', 'medium', 'active',
    '{"adapter": "github_trending", "language": "python"}'
  )
ON CONFLICT DO NOTHING;
