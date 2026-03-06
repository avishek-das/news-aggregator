-- Seed: all Phase 1 sources
-- Run after migrations. Safe to run multiple times (ON CONFLICT DO NOTHING).

INSERT INTO sources (name, url, type, category, priority, status, fetch_config)
VALUES
  -- Phase 1.2 sources
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
  -- Phase 1.4 sources
  (
    'arXiv cs.LG/CL/CV/stat.ML',
    'https://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&max_results=30',
    'api', 'research', 'high', 'active',
    '{"adapter": "arxiv_extra", "categories": ["cs.LG", "cs.CL", "cs.CV", "stat.ML"], "max_results": 30}'
  ),
  (
    'Reddit r/MachineLearning',
    'https://www.reddit.com/r/MachineLearning.json?limit=50&t=day',
    'api', 'community', 'high', 'active',
    '{"adapter": "reddit", "subreddits": ["MachineLearning"], "min_score": 50}'
  ),
  (
    'Reddit r/LocalLLaMA',
    'https://www.reddit.com/r/LocalLLaMA.json?limit=50&t=day',
    'api', 'community', 'medium', 'active',
    '{"adapter": "reddit", "subreddits": ["LocalLLaMA"], "min_score": 30}'
  ),
  (
    'Reddit r/artificial',
    'https://www.reddit.com/r/artificial.json?limit=50&t=day',
    'api', 'community', 'medium', 'active',
    '{"adapter": "reddit", "subreddits": ["artificial"], "min_score": 20}'
  ),
  (
    'Papers with Code',
    'https://paperswithcode.com/latest.rss',
    'rss', 'research', 'high', 'active',
    '{"adapter": "papers_with_code"}'
  ),
  (
    'HuggingFace Daily Papers',
    'https://huggingface.co/api/daily_papers',
    'api', 'research', 'high', 'active',
    '{"adapter": "huggingface"}'
  ),
  (
    'Lobsters AI',
    'https://lobste.rs/t/ai.rss',
    'rss', 'community', 'medium', 'active',
    '{"adapter": "lobsters", "tags": ["ai", "llm", "nlp"]}'
  ),
  (
    'AI Lab Blogs',
    'https://openai.com/blog/rss.xml',
    'rss', 'research', 'high', 'active',
    '{"adapter": "lab_blogs", "feeds": [{"name": "OpenAI", "url": "https://openai.com/blog/rss.xml"}, {"name": "Anthropic", "url": "https://www.anthropic.com/rss.xml"}, {"name": "DeepMind", "url": "https://deepmind.google/blog/rss.xml"}, {"name": "Meta AI", "url": "https://ai.meta.com/blog/rss/"}, {"name": "Mistral", "url": "https://mistral.ai/feed.xml"}]}'
  ),
  (
    'GitHub Trending Python',
    'https://github.com/trending/python?since=daily',
    'scrape', 'code', 'medium', 'active',
    '{"adapter": "github_trending", "language": "python"}'
  ),
  (
    'GitHub Trending Jupyter',
    'https://github.com/trending/jupyter-notebook?since=daily',
    'scrape', 'code', 'medium', 'active',
    '{"adapter": "github_trending", "language": "jupyter-notebook"}'
  ),
  (
    'YouTube AI Channels',
    'https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg',
    'rss', 'media', 'medium', 'active',
    '{"adapter": "youtube", "channels": [{"name": "Two Minute Papers", "channel_id": "UCbfYPyITQ-7l4upoX8nvctg"}, {"name": "Yannic Kilcher", "channel_id": "UCZHmQk67mSJgfCCTn7xBfew"}, {"name": "3Blue1Brown", "channel_id": "UCYO_jab_esuFRV4b17AJtAw"}]}'
  ),
  (
    'AI Podcasts',
    'https://lexfridman.com/feed/podcast/',
    'rss', 'media', 'medium', 'active',
    '{"adapter": "podcasts", "feeds": [{"name": "Lex Fridman Podcast", "url": "https://lexfridman.com/feed/podcast/"}, {"name": "TWIML AI Podcast", "url": "https://feeds.megaphone.fm/MLN2155636147"}, {"name": "Latent Space", "url": "https://api.substack.com/feed/podcast/1084089/s/89348.rss"}]}'
  ),
  (
    'OpenReview Conferences',
    'https://api2.openreview.net/notes',
    'api', 'research', 'medium', 'active',
    '{"adapter": "openreview", "venues": ["ICML.cc/2025/Conference", "NeurIPS.cc/2025/Conference", "ICLR.cc/2025/Conference"]}'
  )
ON CONFLICT DO NOTHING;
