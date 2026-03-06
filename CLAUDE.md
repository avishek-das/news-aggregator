# AI News Aggregator — Claude Session Guide

> This file is the single source of truth for all architectural decisions, implementation plans, and session rules.
> **ideas-v2.md** is the product scope reference. This file is the engineering reference.

---

## Project Summary

A distraction-free news aggregator that surfaces personally relevant AI content from dozens of sources (arXiv, HN, Reddit, GitHub, Hugging Face, lab blogs, etc.) without the user needing to visit those platforms. The value is curation and filtering, not content hosting. Each item shows title, excerpt, source badge, and a direct link to the original.

---

## Confirmed Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     AWS (us-east-1)                     │
│                                                         │
│  ┌──────────────┐    REST     ┌──────────────────────┐  │
│  │  AWS Amplify │ ──────────► │  ALB (public subnet) │  │
│  │  (Next.js)   │             └──────────┬───────────┘  │
│  └──────────────┘                        │              │
│                                          ▼              │
│                              ┌───────────────────────┐  │
│                              │  ECS Fargate (private) │  │
│                              │  FastAPI + Python      │  │
│                              └──────────┬────────────┘  │
│                                         │               │
│  ┌───────────────────────────────────── │ ──────────┐   │
│  │  ECS Scheduled Tasks (daily cron)    │           │   │
│  │  └─ fetch-sources job                │           │   │
│  │  └─ summarize-items job              │           │   │
│  └──────────────────────────────────────┼───────────┘   │
│                                         │               │
│  ┌──────────────────────────────────────┼───────────┐   │
│  │  AWS Secrets Manager                 │           │   │
│  │  (API keys, Supabase conn string)    │           │   │
│  └──────────────────────────────────────┼───────────┘   │
│                                         │               │
│  ┌──────────────────────────────────────┼───────────┐   │
│  │  ECR (Docker image registry)         │           │   │
│  └──────────────────────────────────────┼───────────┘   │
└─────────────────────────────────────────┼───────────────┘
                                          │
                              ┌───────────┴────────────┐
                              │  Supabase (external)   │
                              │  PostgreSQL + Auth      │
                              └────────────────────────┘
```

---

## Confirmed Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | Next.js 14 (App Router) + TypeScript | Static export — no SSR needed since Python serves API |
| Frontend hosting | AWS Amplify | Managed Next.js on AWS, auto HTTPS |
| Styling | Tailwind CSS | Mobile-first utility classes |
| Backend | FastAPI (Python) | Async, auto OpenAPI docs, optimal for ingestion pipelines |
| Backend hosting | ECS Fargate (private subnet) behind ALB | Managed containers, no server ops |
| Database | Supabase (managed Postgres) | Managed DB + Auth + RLS in one |
| Auth (Phase 2) | Supabase Auth (Google OAuth) + FastAPI JWT middleware | Zero custom OAuth code; RLS integrates natively |
| Background jobs | ECS Scheduled Tasks (daily) | Reuses existing FastAPI container |
| LLM abstraction | LiteLLM | Single interface to Gemini, Claude, OpenRouter, 100+ models |
| Dev/test LLM | Gemini Flash 1.5 (free) | Zero cost during development |
| Prod LLM (bulk) | Claude Haiku 4.5 | Cost-efficient bulk summarization |
| Prod LLM (high-signal) | Claude Sonnet 4.6 | Quality for important items |
| Daily prod LLM cost cap | $1/day (configurable via env var) | Stops batch job gracefully when exceeded |
| Unit/Integration tests | Pytest (backend) + Vitest + Testing Library (frontend) | |
| E2E tests | Playwright | Mobile viewport simulation required |
| Container registry | AWS ECR (us-east-1) | |
| Secret management | AWS Secrets Manager | API keys, Supabase conn string |
| CI/CD | GitHub Actions → ECR → ECS (OIDC) | No long-lived AWS credentials in GitHub |
| AWS region | us-east-1 | |
| Domain | Auto-generated Amplify URL + ALB DNS (custom domain later) | |

---

## Development Rules (MANDATORY — enforce on every task)

### Rule 1: Plan before any code

Every sub-phase starts with `planner` + `architect` agents run in **parallel**, producing:
- Requirements restatement
- System / component design with file/folder structure
- Risk assessment (HIGH / MEDIUM / LOW)
- Ordered task breakdown

**No code is written until the plan is confirmed by the user.**

### Rule 2: TDD — tests first, always

Every feature follows RED → GREEN → REFACTOR:
1. Write the failing test
2. Write minimal code to pass
3. Refactor without breaking
4. Verify 80%+ coverage before moving on

Use `tdd-guide` agent for every feature and bug fix.

### Rule 3: Verification before gate

Before closing any sub-phase:
```
Build → Type Check → Lint → Tests (80%+) → Security Scan → Diff Review
```
All must pass. Gate is not cleared until every check is green.

### Rule 4: Small iterations, real feedback

Each sub-phase produces something openable in a browser or verifiable in the DB. No big-bang integrations.

### Rule 5: Security is not optional

- `security-reviewer` mandatory before any gate touching auth, API keys, or user data
- No hardcoded secrets — ever — all secrets in AWS Secrets Manager, loaded as env vars in ECS tasks
- Rate limiting on all API endpoints from Phase 1.2 onward

### Rule 6: Mobile is the primary target

- Build every UI component at 375px first
- Verify on real mobile viewport before marking a UI task done
- E2E tests always include a 375px mobile viewport case

### Rule 7: Model switching must always work

- All LLM calls go through LiteLLM — never call a provider SDK directly
- Active model controlled by `LLM_MODEL` env var
- Dev default: `gemini/gemini-1.5-flash`
- Prod default: `claude-haiku-4-5` (bulk), `claude-sonnet-4-6` (high-signal)

---

## Phase Tracker

| Sub-phase | Goal | Status | Completed |
|-----------|------|--------|-----------|
| 1.1 | Foundation — scaffold, CI, DB schema | ✅ Done | 2026-03-05 |
| 1.2 | First data — arXiv + HN live | ✅ Done | 2026-03-05 |
| 1.3 | First UI — feed on screen | ✅ Done | 2026-03-05 |
| 1.4 | Source expansion — all major sources | ✅ Done | 2026-03-05 |
| 1.5 | Source management — full CRUD + health | Not started | — |
| 1.6 | AI summarization — nightly batch | Not started | — |
| 2.1 | Personalization — feedback + ranking | Not started | — |
| 2.2 | Auth — Google OAuth via Supabase | Not started | — |
| 2.3 | Per-user data — isolated feeds + settings | Not started | — |
| 2.4 | Production hardening | Not started | — |

**Phase 2 does not start until Phase 1 is stable and in active personal use for several weeks.**

### Phase 1.4 — What was built (commit `51e0486`)

- `backend/app/adapters/rss_parser.py` — shared RSS 2.0 + Atom parser; no duplication across adapters
- `backend/app/adapters/arxiv_extra.py` — cs.LG/CL/CV/stat.ML; inherits ArxivAdapter._parse()
- `backend/app/adapters/papers_with_code.py` — RSS with follow_redirects
- `backend/app/adapters/lobsters.py` — multi-tag RSS; URL deduplication across tags
- `backend/app/adapters/lab_blogs.py` — multi-feed RSS; per-feed failure isolation
- `backend/app/adapters/youtube.py` — YouTube Atom feeds; yt:/media: namespace handling
- `backend/app/adapters/podcasts.py` — RSS + itunes:duration enrichment
- `backend/app/adapters/reddit.py` — JSON API; min_score filter; User-Agent; 1s delay between subs
- `backend/app/adapters/huggingface.py` — HF Daily Papers JSON API
- `backend/app/adapters/openreview.py` — OpenReview v2 API; multi-venue
- `backend/app/adapters/github_trending.py` — stdlib HTMLParser; safe empty return on unexpected HTML
- 138 unit tests, 93.85% coverage
- 13 new sources seeded to Supabase; live fetch verified
- `supabase/migrations/002_tracked_researchers.sql` added
- **Known issues**: Papers with Code RSS redirects to HF (source set to inactive); some lab blog URLs need updating

### Phase 1.3 — What was built (commit `3720bc5`)

- `frontend/src/types/item.ts` — `FeedItem`, `Meta`, `ItemsListResponse`, `Category` types
- `frontend/src/lib/constants.ts` — `API_BASE_URL`, `CATEGORIES`, `DEFAULT_LIMIT`
- `frontend/src/lib/time-ago.ts` — pure relative time formatter (testable via `now` param)
- `frontend/src/lib/api.ts` — `fetchItems` + `markRead` with `credentials: 'include'`
- `frontend/src/hooks/use-items.ts` — fetch, paginate, filter, mark-read; abort on category change; `hasMore` via `meta.total`
- `frontend/src/hooks/use-intersection.ts` — `IntersectionObserver` hook for infinite scroll
- `frontend/src/components/SkeletonCard.tsx` — animated pulse loading placeholder
- `frontend/src/components/CategoryTabs.tsx` — All | Research | Code | Community | Product | Media tabs
- `frontend/src/components/ItemCard.tsx` — title link, excerpt, badges, relative time, mark-read on click
- `frontend/src/components/FeedList.tsx` — orchestrates full feed: tabs, states, cards, infinite scroll sentinel
- `frontend/app/page.tsx` — sticky header + FeedList
- `frontend/tsconfig.json` — paths updated: `@/*` → `["./src/*", "./*"]`
- 48 unit tests, 95.83% statement / 98.01% line coverage
- `next build` → static export passes

### Phase 1.2 — What was built (commit `19854ac`)

- `backend/app/adapters/base.py` — `RawItem` frozen dataclass + `SourceAdapter` ABC
- `backend/app/adapters/arxiv.py` — Atom XML parser; fetches cs.AI feed
- `backend/app/adapters/hackernews.py` — Algolia HN API; filters by min_score
- `backend/app/adapters/__init__.py` — `ADAPTER_REGISTRY` + `get_adapter()` factory
- `backend/app/db/client.py` — lazy Supabase singleton (service key)
- `backend/app/models/item.py` — `ItemResponse` + `ItemsListResponse` (frozen Pydantic)
- `backend/app/models/source.py` — `Source` Pydantic model (frozen)
- `backend/app/repositories/sources.py` — `find_active`, `record_success`, `record_failure` (auto-flag after 3 failures)
- `backend/app/repositories/items.py` — `upsert` (on_conflict=url), `find_all` two-query merge
- `backend/app/middleware/session.py` — UUID4 httpOnly cookie, 1-year, SameSite=Lax
- `backend/app/routers/items.py` — `GET /items` (filter, paginate), `POST /items/{id}/read`
- `backend/app/jobs/fetch_sources.py` — daily fetch job; runnable as `python -m app.jobs.fetch_sources`
- 64 unit tests, 92.26% coverage
- **Live integration verified**: 120 items in Supabase (50 arXiv cs.AI + 70 HN)
- GitHub Trending source set to `inactive` until Phase 1.4 adapter is built

### Phase 1.1 — What was built (commit `a46684e`)

- Monorepo: `frontend/` (Next.js 14 static export) + `backend/` (FastAPI)
- `backend/app/config.py` — pydantic-settings, fail-fast on missing vars
- `backend/app/routers/health.py` — `GET /health`, ALB-ready
- `backend/app/main.py` — CORS with `allow_credentials=True` + explicit origins
- `backend/tests/` — 6 unit tests passing (config + health)
- `frontend/__tests__/smoke.test.tsx` — 1 unit test passing
- `supabase/migrations/001_initial_schema.sql` — applied to Supabase ✓
- `supabase/seed.sql` — 3 test sources seeded ✓
- `docker-compose.yml` — local dev (FastAPI + Postgres)
- `.github/workflows/backend-ci.yml` + `frontend-ci.yml` — CI pipelines live
- `infrastructure/` — Terraform: ECR, GitHub OIDC role, Secrets Manager definitions
- `.env.example` — all keys documented

---

## Monorepo Structure

```
news-aggregator/
  frontend/                   — Next.js 14 static export
    app/
      page.tsx                — Feed page
      layout.tsx              — Root layout + theme provider
      sources/
        page.tsx              — Source list
        new/page.tsx          — Add source form
        [id]/edit/page.tsx    — Edit source
        health/page.tsx       — Health dashboard
      settings/page.tsx       — User settings (Phase 2)
      login/page.tsx          — Google OAuth login (Phase 2)
    components/
      FeedList.tsx
      ItemCard.tsx
      CategoryTabs.tsx
      SkeletonCard.tsx
      SourceBadge.tsx
      BottomNav.tsx
      Sidebar.tsx
    lib/
      api.ts                  — REST calls to FastAPI backend
      session.ts              — Anonymous session helpers (Phase 1)
    __tests__/
    public/
    next.config.ts            — output: 'export' (static)
    tailwind.config.ts
    vitest.config.ts
    playwright.config.ts

  backend/                    — FastAPI (Python)
    app/
      main.py                 — FastAPI app, CORS, router registration
      routers/
        items.py              — GET /items, GET /items/{id}
        sources.py            — CRUD /sources
        feedback.py           — POST /feedback (Phase 2)
        health.py             — GET /health (liveness probe)
      adapters/
        base.py               — SourceAdapter abstract base class
        arxiv.py
        hackernews.py
        reddit.py
        github_trending.py
        papers_with_code.py
        huggingface.py
        lobsters.py
        lab_blogs.py          — Phase 1.4
        youtube.py            — Phase 1.4
        podcasts.py           — Phase 1.4
        openreview.py         — Phase 1.4
      repositories/
        items.py
        sources.py
        sessions.py           — Anonymous session read-state (Phase 1)
      jobs/
        fetch_sources.py      — Daily fetch job (entry point for ECS task)
        summarize_items.py    — Nightly summarization job
      services/
        summarize.py          — LiteLLM summarization service
        ranking.py            — Feed ranking (Phase 2)
        dedup.py              — URL deduplication helpers
      middleware/
        auth.py               — Supabase JWT verification (Phase 2)
        rate_limit.py
      models/
        source.py             — Pydantic models
        item.py
        feedback.py
      db/
        client.py             — Supabase Python client
      config.py               — Settings loaded from env vars / Secrets Manager
    tests/
      unit/
      integration/
    Dockerfile
    requirements.txt
    pyproject.toml            — Pytest config, ruff, mypy

  supabase/
    migrations/               — SQL migration files (numbered)
    seed.sql                  — Dev seed data

  infrastructure/
    ecr.tf                    — ECR repository
    ecs.tf                    — ECS cluster, task definitions, services
    alb.tf                    — ALB, target groups, listeners
    iam.tf                    — Task execution role, OIDC role for GitHub Actions
    secrets.tf                — Secrets Manager secret definitions
    variables.tf              — VPC ID, subnet IDs (placeholders)
    outputs.tf

  .github/
    workflows/
      backend-ci.yml          — Lint + type-check + test on PR
      frontend-ci.yml         — Lint + type-check + test on PR
      deploy-backend.yml      — Push to ECR + update ECS on merge to main
      deploy-frontend.yml     — Amplify deploy on merge to main

  docker-compose.yml          — Local dev: FastAPI + Postgres
  .env.example                — All env var keys, no values
  ideas-v2.md
  CLAUDE.md
```

---

## Detailed Implementation Plan

### Phase 1.1 — Foundation

**Goal:** Monorepo scaffold, CI pipelines, DB schema, local dev environment. Nothing visible yet.

**Before coding:** Run `planner` + `architect` in parallel. Produce ADR confirming tech stack.

**Tasks:**

1. Initialize monorepo
   - `frontend/` — `npx create-next-app@latest` with App Router + TypeScript + Tailwind
   - Set `output: 'export'` in `next.config.ts` (static export — no SSR needed)
   - `backend/` — FastAPI project with `uv` or `pip`, `pyproject.toml`, `ruff`, `mypy`, `pytest`
   - `docker-compose.yml` for local dev (FastAPI + local Postgres for dev only)
   - Test: `npm run build` (frontend) and `uvicorn app.main:app` (backend) both pass

2. CI pipelines (GitHub Actions)
   - `backend-ci.yml`: ruff lint → mypy type-check → pytest on every PR
   - `frontend-ci.yml`: ESLint → tsc → vitest on every PR
   - Test: both pipelines green on empty commit

3. AWS infrastructure baseline (Terraform in `infrastructure/`)
   - ECR repository for backend Docker image
   - Placeholder variables for VPC ID and subnet IDs (fill in during deployment)
   - IAM OIDC provider for GitHub Actions (see GitHub → AWS OIDC setup below)
   - IAM role: `github-actions-deployer` with ECR push + ECS update permissions
   - Secrets Manager secret placeholders (values added manually before first deploy)

4. Supabase project setup
   - Create project at supabase.com
   - Add connection string to AWS Secrets Manager as `news-aggregator/supabase-db-url`
   - Add anon key as `news-aggregator/supabase-anon-key`
   - Add service role key as `news-aggregator/supabase-service-key`

5. DB schema — migration 001
   ```sql
   CREATE EXTENSION IF NOT EXISTS "pgcrypto";

   CREATE TABLE categories (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     name text NOT NULL,
     slug text NOT NULL UNIQUE
   );

   CREATE TABLE sources (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     name text NOT NULL,
     url text NOT NULL,
     type text NOT NULL CHECK (type IN ('rss','api','scrape')),
     category text NOT NULL,
     priority text NOT NULL DEFAULT 'medium'
       CHECK (priority IN ('high','medium','low')),
     status text NOT NULL DEFAULT 'active'
       CHECK (status IN ('active','inactive','flagged')),
     fetch_config jsonb NOT NULL DEFAULT '{}',
     last_fetched_at timestamptz,
     last_error text,
     consecutive_failures int NOT NULL DEFAULT 0,
     created_at timestamptz NOT NULL DEFAULT now()
   );

   CREATE TABLE items (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     source_id uuid NOT NULL REFERENCES sources(id),
     title text NOT NULL,
     url text NOT NULL UNIQUE,
     excerpt text,
     summary text,
     published_at timestamptz,
     category text NOT NULL,
     is_paywalled boolean NOT NULL DEFAULT false,
     raw_metadata jsonb NOT NULL DEFAULT '{}',
     created_at timestamptz NOT NULL DEFAULT now()
   );

   CREATE TABLE user_sessions (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     session_id text NOT NULL UNIQUE,
     created_at timestamptz NOT NULL DEFAULT now(),
     last_seen_at timestamptz NOT NULL DEFAULT now()
   );

   CREATE TABLE read_items (
     session_id text NOT NULL,
     item_id uuid NOT NULL REFERENCES items(id),
     read_at timestamptz NOT NULL DEFAULT now(),
     PRIMARY KEY (session_id, item_id)
   );

   -- Seed categories
   INSERT INTO categories (name, slug) VALUES
     ('Research', 'research'),
     ('Code', 'code'),
     ('Community', 'community'),
     ('Product', 'product'),
     ('Media', 'media');
   ```
   - Test: migration runs cleanly, rollback verified

6. Seed 3 test sources
   - arXiv cs.AI (api, research, high)
   - Hacker News (api, community, high)
   - GitHub Trending (scrape, code, medium)
   - Test: `SELECT * FROM sources` returns 3 rows

7. FastAPI `config.py` — loads all env vars/secrets at startup, fails fast if missing
   - Test: missing required env var → startup error with clear message

**Gate:** Both builds pass. CI green. DB migrated + rollback verified. ADR written and confirmed.

---

### Phase 1.2 — First Data: Two Sources Live

**Goal:** Real data from arXiv + Hacker News. Verify via DB or `GET /items`.

**Before coding:** Run `planner`. Define adapter interface first, before any implementation.

**Adapter contract (define before implementing):**
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawItem:
    title: str
    url: str
    excerpt: str
    published_at: datetime
    category: str
    is_paywalled: bool = False
    raw_metadata: dict = field(default_factory=dict)

class SourceAdapter(ABC):
    source_id: str

    @abstractmethod
    async def fetch(self) -> list[RawItem]:
        ...
```

**Tasks:**

1. arXiv adapter (`adapters/arxiv.py`)
   - Use arXiv API: `https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate`
   - Parse Atom XML response → `list[RawItem]`
   - Unit test: parse fixture XML → correct `RawItem` list

2. Hacker News adapter (`adapters/hackernews.py`)
   - Algolia HN API: `https://hn.algolia.com/api/v1/search?tags=story&query=AI`
   - Filter: score > 10, contains AI/ML keywords in title
   - Unit test: mock API response → filtered `RawItem` list

3. `ItemRepository` (`repositories/items.py`)
   - `async def upsert(items: list[RawItem], source_id: str) -> int` — inserts new, skips duplicates by URL
   - `async def find_all(category=None, limit=10, offset=0) -> list[Item]`
   - Unit test: upsert same URL twice → one row; returns correct count

4. Daily fetch job (`jobs/fetch_sources.py`)
   - Entry point: reads active sources from DB, instantiates correct adapter, calls `fetch()`, calls `upsert()`
   - Runs as ECS Scheduled Task (daily at 06:00 UTC)
   - Integration test: run job with test DB → items appear

5. Deduplication
   - Unique constraint on `items.url` at DB level (migration 001 already has it)
   - Repository catches `UniqueViolation` and skips gracefully
   - Unit test: upsert duplicate → no exception, returns 0 new items

6. Source failure tracking
   - On fetch error: increment `consecutive_failures`, set `last_error`
   - On success: reset `consecutive_failures = 0`, update `last_fetched_at`
   - Unit test: error path → fields updated correctly

7. `GET /items` endpoint
   - Query params: `category`, `source_id`, `limit` (default 10), `offset`
   - Response: `{ success: true, data: [...], meta: { total, page, limit } }`
   - Integration test: items in DB → GET returns correct shape

**Gate:** arXiv + HN live data in DB. Dedup works. 80%+ coverage on ingestion. `code-reviewer` signed off.

---

### Phase 1.3 — First UI: Feed on Screen

**Goal:** Real, usable feed page. Open on your phone — feels like a product.

**Before coding:** Run `planner`. Wireframe mobile layout before any component work.

**Key decisions:**
- Next.js static export calls FastAPI via `NEXT_PUBLIC_API_URL` env var
- No Next.js API routes (Python handles all API)
- Anonymous session: generated UUID stored in httpOnly cookie, sent with every request

**Frontend API client (`frontend/lib/api.ts`):**
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function getItems(params: {
  category?: string
  limit?: number
  offset?: number
}): Promise<{ data: Item[]; meta: Meta }> { ... }

export async function markRead(itemId: string): Promise<void> { ... }
```

**Tasks:**

1. `ItemCard` component
   - Props: `title`, `url`, `sourceName`, `category`, `publishedAt`, `excerpt`, `isPaywalled`, `isRead`
   - External link: `target="_blank" rel="noopener noreferrer"`
   - Paywalled items show title + `[Paywalled]` badge, still linkable
   - Read items visually dimmed (opacity)
   - On click: call `markRead()`, open URL
   - E2E: card renders, click → URL opened, card dims

2. `FeedList` with infinite scroll
   - Loads 10 items per page
   - IntersectionObserver triggers next page load
   - E2E: scroll to bottom → next 10 items load

3. Mobile layout (375px) — primary
   - Single column feed
   - `BottomNav` — Feed / Sources / Settings tabs
   - Minimum 44px tap targets
   - No horizontal scroll
   - E2E at 375px

4. Desktop layout (1280px)
   - Persistent left sidebar: `CategoryTabs` + source list
   - Feed in center column
   - E2E at 1280px

5. Dark / light mode
   - `next-themes` — follows `prefers-color-scheme`, no flash on load
   - Manual toggle in header

6. `SkeletonCard` — shows while data fetches
   - E2E: skeletons visible before real cards on simulated slow network

7. `CategoryTabs`
   - All / Research / Code / Community / Product / Media
   - Selected tab re-fetches with `category` filter
   - E2E: select Research → only research items

8. Anonymous session (Phase 1 read tracking)
   - FastAPI middleware: if no `session_id` cookie, generate UUID, set httpOnly cookie (30-day expiry)
   - `POST /items/{id}/read` — records `(session_id, item_id)` in `read_items`
   - `GET /items` — joins `read_items` by session_id, returns `is_read` flag per item
   - E2E: click item → re-fetch shows it dimmed

**Gate:** Feed loads live data on mobile and desktop. Works on a real phone. All E2E tests pass. No horizontal scroll. `code-reviewer` signed off.

---

### Phase 1.4 — Source Expansion: All Major Sources

**Goal:** All remaining Phase 1 sources wired up. Category auto-tagging.

**Before coding:** Run `planner`. Confirm adapter pattern extends cleanly.

**New adapters:**

| Adapter | Source | Method | Category | Priority |
|---------|--------|--------|----------|----------|
| `reddit.py` | r/MachineLearning, r/LocalLLaMA, r/artificial | Reddit JSON API | community | medium |
| `github_trending.py` | GitHub Trending (Python, ML topics) | HTML scrape | code | medium |
| `papers_with_code.py` | Papers with Code | RSS | research | medium |
| `huggingface.py` | HF new models, trending | HF API | code | medium |
| `lobsters.py` | Lobsters (ai, llm, nlp tags) | RSS | community | medium |
| `lab_blogs.py` | OpenAI, Anthropic, DeepMind, Meta AI, Mistral blogs | RSS | research | high |
| `arxiv_extra.py` | cs.LG, cs.CL, cs.CV, stat.ML | arXiv API | research | high |
| `youtube.py` | Karpathy, Kilcher, Two Minute Papers, etc. | YouTube RSS | media | low |
| `podcasts.py` | Lex Fridman, TWIML, Latent Space, etc. | RSS | media | low |
| `openreview.py` | Papers under review at ICML, NeurIPS, ICLR | OpenReview API | research | low |

**Tasks:**

1. Build each adapter following `SourceAdapter` interface
   - One file per adapter
   - Integration test per adapter: live fetch returns non-empty `list[RawItem]`

2. Adapter registry (`adapters/__init__.py`)
   - Maps `source.type + source.fetch_config['adapter']` → adapter class
   - Fetch job dynamically instantiates correct adapter from registry
   - Unit test: registry returns correct class for each source type

3. Category auto-tagging in each adapter
   - Tag set at adapter level, not inferred at runtime
   - Unit test: item from `arxiv.py` → `category = "research"`

4. Register all new sources in seed SQL
   - `supabase/seed.sql` updated with all sources
   - Sources stored in DB — job reads from DB, not hardcoded

5. `CategoryTabs` in UI already handles all categories (no UI change needed if tabs use dynamic category list)

6. Paywalled flag
   - Sources that are known paywalled: flag `is_paywalled = True` in adapter
   - UI: `[Paywalled]` badge on card

7. Researcher tracking (configurable via UI — Phase 1.4 adds DB schema only)
   ```sql
   CREATE TABLE tracked_researchers (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     name text NOT NULL,
     identifiers jsonb NOT NULL DEFAULT '{}',
     -- e.g. {"semantic_scholar_id": "...", "twitter_handle": "..."}
     created_at timestamptz NOT NULL DEFAULT now()
   );
   ```
   - Adapter integrations (Semantic Scholar, etc.) use this table — Phase 1.4+ builds

8. Regression: all previously passing tests pass
   - Full verification loop before gate

**Gate:** All sources ingesting. Category filters correct. Paywalled flag works. No regressions. 80%+ coverage. `code-reviewer` signed off.

---

### Phase 1.5 — Source Management: Full CRUD + Health

**Goal:** Admin UI to add, edit, retire, reactivate sources. Health monitoring.

**Tasks:**

1. FastAPI CRUD endpoints for sources
   - `GET /sources` — list with status, last fetch, error
   - `POST /sources` — add new source
   - `PATCH /sources/{id}` — edit fields (takes effect next fetch cycle)
   - `POST /sources/{id}/retire` — sets `status = inactive`
   - `POST /sources/{id}/reactivate` — sets `status = active`
   - Integration tests for each

2. Health monitor in fetch job
   - After 3 consecutive failures → `status = flagged`
   - Unit test: 3 errors → `status = "flagged"`, `last_error` set

3. Source list page (`/sources`)
   - Table: name, category, priority, status, last fetched, error
   - Status badge: active (green) / inactive (grey) / flagged (red)
   - Action buttons: Edit / Retire / Reactivate

4. Add source form (`/sources/new`)
   - Fields: name, URL, adapter type, category, priority
   - E2E: submit → source in list

5. Edit source form (`/sources/[id]/edit`)
   - Pre-populated, any field editable
   - Integration test: change URL → next fetch uses new URL

6. Health dashboard (`/sources/health`)
   - Shows only flagged sources
   - Last error + timestamp + Reactivate button
   - E2E: flagged source visible with error detail

**Gate:** Full CRUD works in UI. Health auto-flags. History preserved on retire. All tests pass. `code-reviewer` signed off.

---

### Phase 1.6 — AI Summarization: Nightly Batch

**Goal:** Summaries on cards. Cost-controlled, batched, model-switchable.

**Before coding:** Run `security-reviewer` before implementation — LLM API key handling.

**LiteLLM setup (`services/summarize.py`):**
```python
import litellm

async def summarize(excerpt: str, model: str | None = None) -> str:
    active_model = model or settings.LLM_MODEL  # from env var
    response = await litellm.acompletion(
        model=active_model,
        messages=[{
            "role": "user",
            "content": f"Summarize in 2-3 sentences. Include source links if present.\n\n{excerpt}"
        }],
        max_tokens=150
    )
    return response.choices[0].message.content
```

**Env vars for model switching:**
```
LLM_MODEL=gemini/gemini-1.5-flash          # dev default (free)
LLM_MODEL=claude-haiku-4-5-20251001        # prod bulk
LLM_HIGH_SIGNAL_MODEL=claude-sonnet-4-6    # prod high-signal
DAILY_LLM_COST_CAP_USD=1.00               # configurable, stops job when exceeded
```

**Tasks:**

1. `summarize()` service via LiteLLM
   - Unit test: mock LiteLLM → summary stored, correct model called

2. Cost tracker (`services/cost_tracker.py`)
   - Reads `litellm.completion_cost()` after each call
   - Accumulates daily total in `job_runs` table
   - Raises `DailyCostCapExceeded` when total exceeds `DAILY_LLM_COST_CAP_USD`
   - Unit test: cost exceeds cap → exception raised, job stops

3. `job_runs` table (migration 002)
   ```sql
   CREATE TABLE job_runs (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     job_name text NOT NULL,
     run_date date NOT NULL,
     items_processed int NOT NULL DEFAULT 0,
     tokens_used int NOT NULL DEFAULT 0,
     cost_usd numeric(10,6) NOT NULL DEFAULT 0,
     status text NOT NULL DEFAULT 'running',
     completed_at timestamptz,
     created_at timestamptz NOT NULL DEFAULT now(),
     UNIQUE (job_name, run_date)
   );
   ```

4. Nightly batch job (`jobs/summarize_items.py`)
   - Scheduled: 02:00 UTC daily (ECS Scheduled Task)
   - Fetch items where `summary IS NULL`, batch 50 at a time
   - On `DailyCostCapExceeded`: log warning, mark job complete, stop gracefully
   - Integration test: job runs → items get summaries; cost cap stops job

5. Fallback in UI: `summary ?? excerpt` — never a blank card
   - E2E: item without summary → excerpt shown

6. Expandable summary on card
   - Default: collapsed (excerpt)
   - "Show summary" → summary expands inline
   - E2E: tap expand → summary visible

**Gate:** Summaries on live cards. Batch runs on schedule. Cost cap works. No LLM API key in frontend. `security-reviewer` signed off.

---

### Phase 2.1 — Personalization & Feedback

**Goal:** Thumbs up/down on items. Feed adapts after ~5 signals.

**Tasks:**

1. `item_feedback` table (migration 003)
   ```sql
   CREATE TABLE item_feedback (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     session_id text NOT NULL,          -- Phase 1: anonymous; Phase 2: user_id
     item_id uuid NOT NULL REFERENCES items(id),
     signal text NOT NULL CHECK (signal IN ('up','down','dismiss')),
     created_at timestamptz NOT NULL DEFAULT now(),
     UNIQUE (session_id, item_id)
   );
   ```

2. `POST /feedback` endpoint
   - Body: `{ item_id, signal }`
   - Uses `session_id` from cookie
   - E2E: click thumbs up → row in `item_feedback`

3. Thumbs up / down on desktop `ItemCard`
4. Swipe right (up) / left (dismiss) on mobile with `@use-gesture/react`
   - E2E at 375px: swipe → signal recorded

5. Ranking function (`services/ranking.py`)
   - Pure function: `rank(items, feedback_signals) -> list[Item]`
   - Items from sources/categories with net positive signals score higher
   - Dismissed items hidden
   - Unit test: known signals → deterministic ordering

6. Feed re-ranks after 5+ interactions
   - Manual check: like 5 research papers → research items rise

**Gate:** Feedback persists. Ranking changes based on signals. Swipe works. Unit tests cover ranking.

---

### Phase 2.2 — User Authentication

**Goal:** Google OAuth sign-in via Supabase Auth. All routes protected.

**Before coding:** Run `architect` + `security-reviewer`.

**Auth flow:**
```
1. User clicks "Sign in with Google" on /login
2. Next.js frontend redirects to Supabase Auth Google OAuth URL
3. User authenticates with Google
4. Supabase issues JWT, redirects back to frontend with session
5. Frontend stores JWT (Supabase client SDK handles this)
6. All API calls include: Authorization: Bearer <supabase-jwt>
7. FastAPI middleware verifies JWT signature against Supabase JWKS endpoint
8. auth.uid() extracted from JWT, used for all DB queries
```

**FastAPI JWT middleware (`middleware/auth.py`):**
```python
from supabase import create_client
import jwt

async def verify_jwt(token: str) -> dict:
    # Verify against Supabase JWKS — one middleware line
    payload = jwt.decode(token, options={"verify_signature": True}, ...)
    return payload  # contains sub = user UUID
```

**Tasks:**

1. `/login` page with Google OAuth button (Supabase client SDK)
2. Supabase Auth: configure Google OAuth provider in Supabase dashboard
3. FastAPI `auth` middleware — verifies Supabase JWT on protected routes
4. Route protection: unauthenticated → 401; frontend redirects to `/login`
5. Sign-out: clears Supabase session, redirects to `/login`
6. E2E: full sign-in → feed; sign-out → login page
7. `security-reviewer` mandatory sign-off

**Gate:** Full auth flow end-to-end. All protected routes return 401 without valid JWT. Security reviewer passes.

---

### Phase 2.3 — Per-User Data

**Goal:** Each user's feedback and settings isolated. RLS enforced.

**Tasks:**

1. Migrate `item_feedback.session_id` → `user_id uuid REFERENCES auth.users(id)` (migration 004)
   - Data migration: existing anonymous feedback deleted (Phase 1 was single-user, no loss)

2. `user_preferences` table (migration 004)
   ```sql
   CREATE TABLE user_preferences (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     user_id uuid NOT NULL REFERENCES auth.users(id),
     key text NOT NULL,
     value jsonb NOT NULL DEFAULT '{}',
     updated_at timestamptz NOT NULL DEFAULT now(),
     UNIQUE (user_id, key)
   );
   ```

3. RLS policies on all user-scoped tables
   ```sql
   ALTER TABLE item_feedback ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "users own feedback" ON item_feedback
     USING (user_id = auth.uid());

   ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "users own preferences" ON user_preferences
     USING (user_id = auth.uid());
   ```
   - Integration test: user A cannot read user B's rows

4. Settings page (`/settings`)
   - Toggle sources on/off per user (stored in `user_preferences`)
   - E2E: disable source → disappears from feed for that user only

5. Scope all feedback queries to `auth.uid()` via FastAPI middleware context

**Gate:** Two test accounts have independent feeds. RLS verified. Migration tested.

---

### Phase 2.4 — Production Hardening

**Goal:** Stable, monitored, production-ready deployment.

**Tasks:**

1. Deployment pipeline
   - Merge to `main` → GitHub Actions → ECR push → ECS service update → Amplify deploy
   - No direct production deploys — always goes through CI

2. Secrets audit
   - `grep -r "sk-" . --include="*.py"` and similar scans
   - All secrets in Secrets Manager, zero in code

3. Rate limiting (`middleware/rate_limit.py`)
   - Use `slowapi` (FastAPI-native) or Redis-backed limiter
   - Per-IP: 60 req/min on public endpoints
   - Integration test: exceed limit → 429

4. Error monitoring — Sentry
   - `sentry-sdk[fastapi]` in backend
   - Sentry SDK in frontend (`@sentry/nextjs`)
   - Test: deliberate error → appears in Sentry

5. Performance: feed loads under 2s on mobile (3G)
   - Lighthouse audit on Amplify URL
   - Optimize bundle, lazy-load images

6. Full verification loop on staging before any prod release

**Gate:** Staging end-to-end. All checks green. Performance budget met. Sentry active.

---

## Full Data Model

```sql
-- Phase 1 — Migration 001 (up)

CREATE TABLE sources (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  url text NOT NULL,
  type text NOT NULL CHECK (type IN ('rss','api','scrape')),
  category text NOT NULL CHECK (category IN ('research','code','community','product','media')),
  priority text NOT NULL DEFAULT 'medium'
    CHECK (priority IN ('high','medium','low')),
  status text NOT NULL DEFAULT 'active'
    CHECK (status IN ('active','inactive','flagged')),
  fetch_config jsonb NOT NULL DEFAULT '{}',
  last_fetched_at timestamptz,
  last_error text,
  consecutive_failures int NOT NULL DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id uuid NOT NULL REFERENCES sources(id),
  title text NOT NULL,
  url text NOT NULL UNIQUE,
  excerpt text,
  summary text,
  published_at timestamptz,
  category text NOT NULL CHECK (category IN ('research','code','community','product','media')),
  is_paywalled boolean NOT NULL DEFAULT false,
  raw_metadata jsonb NOT NULL DEFAULT '{}',
  updated_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE user_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now(),
  last_seen_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE read_items (
  session_id text NOT NULL REFERENCES user_sessions(session_id) ON DELETE CASCADE,
  item_id uuid NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  read_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (session_id, item_id)
);

CREATE TABLE job_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_name text NOT NULL,
  run_date date NOT NULL,
  items_processed int NOT NULL DEFAULT 0,
  tokens_used int NOT NULL DEFAULT 0,
  cost_usd numeric(10,6) NOT NULL DEFAULT 0,
  status text NOT NULL DEFAULT 'running'
    CHECK (status IN ('running','completed','failed')),
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (job_name, run_date)
);

CREATE TABLE tracked_researchers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  identifiers jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Required indexes
CREATE INDEX idx_items_source_id ON items (source_id);
CREATE INDEX idx_items_category_published ON items (category, published_at DESC);
CREATE INDEX idx_items_created_at ON items (created_at DESC);
CREATE INDEX idx_sources_status ON sources (status);
CREATE INDEX idx_read_items_session_id ON read_items (session_id);

-- Note: NO categories table. Category values are enforced via CHECK constraints
-- above. The frontend category list is hardcoded (values change rarely).

-- Phase 2 additions (migration 003+)
-- item_feedback   (id, user_id, item_id, signal, created_at)
-- user_preferences (id, user_id, key, value, updated_at)
```

### Key schema decisions (from architect review)

- **No `categories` table** — category values enforced via `CHECK` constraints on `sources.category` and `items.category`. Frontend hardcodes the list `['research','code','community','product','media']`.
- **`read_items.session_id` has FK** to `user_sessions(session_id)` with `ON DELETE CASCADE` — no orphaned read records.
- **`updated_at` on `sources` and `items`** — tracks edits for audit trail.
- **5 indexes defined in migration 001** — required for feed query performance from day one.

---

## API Design

### Base URL
- Dev: `http://localhost:8000`
- Prod: `https://<alb-dns-name>/` (Amplify frontend sets `NEXT_PUBLIC_API_URL`)

### Response envelope (all endpoints)
```json
{ "success": true,  "data": <T>,   "meta": { "total": 0, "limit": 10, "offset": 0 } }
{ "success": false, "data": null,  "error": "message" }
```

### `GET /health` (Phase 1.1)
```
Response 200:
{ "success": true, "data": { "status": "healthy", "version": "0.1.0", "database": "connected" } }

Response 503 (DB unreachable):
{ "success": false, "data": null, "error": "Database connection failed" }
```
ALB health check targets this endpoint. Must return 200 within 5s.

### `GET /items` (Phase 1.2)
```
Query params: category?, source_id?, limit=10 (max 100), offset=0
Cookie: session_id=<uuid>   (set by middleware on first request)

Item shape:
{
  "id": "uuid",
  "source_id": "uuid",
  "source_name": "arXiv cs.AI",   // joined from sources.name
  "title": "...",
  "url": "https://...",
  "excerpt": "...",
  "summary": null,                 // null until Phase 1.6
  "published_at": "ISO8601",
  "category": "research",
  "is_paywalled": false,
  "is_read": false,                // LEFT JOIN read_items by session_id
  "created_at": "ISO8601"
}
```

### Session cookie contract (CRITICAL — cross-origin)
- FastAPI middleware: if no `session_id` cookie, generate UUID v4, set:
  `Set-Cookie: session_id=<uuid>; HttpOnly; SameSite=Lax; Path=/; Max-Age=2592000`
- Frontend must use `credentials: 'include'` on every fetch call
- FastAPI CORS **must** use `allow_credentials=True` + explicit origins (never `*`)
- Without this, cookies are silently dropped cross-origin

### Endpoints (Phase 1)
```
GET  /health                      — liveness probe (ALB health check)
GET  /items                       — list items (category, source_id, limit, offset)
GET  /items/{id}                  — single item
POST /items/{id}/read             — mark read (uses session cookie)
GET  /sources                     — list sources
POST /sources                     — create source
GET  /sources/{id}                — get source
PATCH /sources/{id}               — update source
POST /sources/{id}/retire         — retire source
POST /sources/{id}/reactivate     — reactivate source
GET  /sources/health              — list flagged sources
```

### Endpoints (Phase 2 additions)
```
POST /feedback                    — submit up/down/dismiss (requires JWT)
GET  /preferences                 — get user preferences (requires JWT)
PUT  /preferences/{key}           — set preference (requires JWT)
```

---

## AWS Infrastructure Details

### GitHub Actions → AWS (OIDC setup — no long-lived credentials)

**Bootstrap (one-time, done manually — chicken-and-egg with Terraform):**
The OIDC provider and initial IAM role must be created manually first (AWS Console or CLI), then imported into Terraform state. Terraform cannot create its own deployer role using itself.

```bash
# One-time bootstrap via AWS CLI
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

**IAM role trust policy** (scope to specific repo + branch):
```json
{
  "Condition": {
    "StringLike": {
      "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/news-aggregator:ref:refs/heads/main"
    }
  }
}
```
- Restrict deploy role to `main` branch only
- CI (lint/test) workflows do NOT need AWS credentials — no role assumption in CI jobs

**GitHub repo secrets required:**
- `AWS_ROLE_ARN` — ARN of `github-actions-deployer` role

**GitHub Actions deploy step:**
```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1
```
No AWS access keys stored anywhere.

### Terraform remote state (setup in Phase 1.1)

Add `infrastructure/backend.tf`:
```hcl
terraform {
  backend "s3" {
    bucket         = "news-aggregator-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "news-aggregator-terraform-locks"
    encrypt        = true
  }
}
```

Bootstrap the S3 bucket and DynamoDB table manually before `terraform init`:
```bash
aws s3 mb s3://news-aggregator-terraform-state --region us-east-1
aws s3api put-bucket-versioning --bucket news-aggregator-terraform-state \
  --versioning-configuration Status=Enabled
aws dynamodb create-table --table-name news-aggregator-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST --region us-east-1
```

### Amplify SPA fallback (REQUIRED for dynamic routes)

In Amplify console → App settings → Rewrites and redirects, add:
```
Source: /<*>
Target: /index.html
Type: 200 (Rewrite)
```
Without this, refreshing `/sources/abc123/edit` returns a 404.

### Supabase from ECS
- ECS tasks (private subnet) connect to Supabase over HTTPS
- Private subnets require NAT Gateway for internet egress (include in Terraform)
- Supabase connection string loaded from Secrets Manager at task startup via ECS secrets injection:
  ```json
  { "name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:us-east-1:...:news-aggregator/supabase-db-url" }
  ```

### ECS Task Definitions
- Backend API: 512 CPU / 1024 MB RAM, 1 container (FastAPI), port 8000
- Fetch job: 256 CPU / 512 MB RAM, same image, `CMD ["python", "-m", "app.jobs.fetch_sources"]`
- Summarize job: 256 CPU / 512 MB RAM, same image, `CMD ["python", "-m", "app.jobs.summarize_items"]`

### ECS Scheduled Tasks (daily cron)
- Fetch sources: `cron(0 6 * * ? *)` — 06:00 UTC daily
- Summarize items: `cron(0 2 * * ? *)` — 02:00 UTC daily

### Secrets Manager keys
```
news-aggregator/supabase-db-url
news-aggregator/supabase-anon-key
news-aggregator/supabase-service-key
news-aggregator/gemini-api-key          # dev/test
news-aggregator/anthropic-api-key       # prod
news-aggregator/reddit-client-id        # Phase 1.4
news-aggregator/reddit-client-secret    # Phase 1.4
```

---

## Multi-Model LLM Config

```
# .env (local dev)
LLM_MODEL=gemini/gemini-1.5-flash
LLM_HIGH_SIGNAL_MODEL=gemini/gemini-1.5-flash
GEMINI_API_KEY=<from google ai studio, free>
DAILY_LLM_COST_CAP_USD=0.00            # $0 cap in dev (Gemini is free)

# Production (Secrets Manager)
LLM_MODEL=claude-haiku-4-5-20251001
LLM_HIGH_SIGNAL_MODEL=claude-sonnet-4-6
ANTHROPIC_API_KEY=<from secrets manager>
DAILY_LLM_COST_CAP_USD=1.00            # $1/day hard cap, configurable
```

LiteLLM reads `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` automatically — no code changes to switch models.

---

## Content Sources Reference

| Source | Adapter | Method | Category | Priority | Phase |
|--------|---------|--------|----------|----------|-------|
| arXiv cs.AI | arxiv.py | API | research | high | 1.2 |
| Hacker News | hackernews.py | Algolia API | community | high | 1.2 |
| arXiv cs.LG, cs.CL, cs.CV, stat.ML | arxiv_extra.py | API | research | high | 1.4 |
| Reddit (r/ML, r/LocalLLaMA, r/artificial) | reddit.py | JSON API | community | medium | 1.4 |
| GitHub Trending (Python, ML) | github_trending.py | scrape | code | medium | 1.4 |
| Papers with Code | papers_with_code.py | RSS | research | medium | 1.4 |
| Hugging Face (models, trending) | huggingface.py | HF API | code | medium | 1.4 |
| Lobsters (ai, llm, nlp) | lobsters.py | RSS | community | medium | 1.4 |
| Lab blogs (OpenAI, Anthropic, DeepMind, Meta AI, Mistral) | lab_blogs.py | RSS | research | high | 1.4 |
| YouTube channels | youtube.py | RSS | media | low | 1.4 |
| Podcasts | podcasts.py | RSS | media | low | 1.4 |
| OpenReview | openreview.py | API | research | low | 1.4 |
| X/Twitter | — | Paid API | community | — | Pending |
| LinkedIn | — | 3rd-party scraper | community | — | Pending |
| Google Scholar | — | 3rd-party scraper | research | — | Pending |
| Discord | — | API (access-dependent) | community | — | Pending |

---

## Agent Workflow

```
Phase kick-off  ->  planner + architect (parallel)
Feature build   ->  tdd-guide -> code-reviewer -> security-reviewer
Pre-gate        ->  e2e-runner
```

| Agent | When |
|-------|------|
| `planner` | Start of every sub-phase |
| `architect` | Tech stack or schema decisions |
| `tdd-guide` | Every new feature or bug fix |
| `code-reviewer` | After every implementation |
| `security-reviewer` | Any gate with auth, API keys, or user data |
| `e2e-runner` | Pre-gate for all UI sub-phases (1.3, 1.4, 1.5, 2.1, 2.2) |
| `build-error-resolver` | When CI or build fails |

## Skills to Activate

| Skill | Sub-phase |
|-------|-----------|
| `everything-claude-code:tdd` | Every feature |
| `everything-claude-code:backend-patterns` | 1.2, 1.4, 1.5 |
| `everything-claude-code:api-design` | 1.2, 1.5, 2.1 |
| `everything-claude-code:frontend-patterns` | 1.3, 1.4, 2.1 |
| `everything-claude-code:database-migrations` | Any schema change |
| `everything-claude-code:postgres-patterns` | 1.4+ |
| `everything-claude-code:cost-aware-llm-pipeline` | 1.6, 2.1 |
| `everything-claude-code:security-review` | 1.6, 2.2, 2.3, 2.4 |
| `everything-claude-code:e2e` | 1.3, 1.4, 1.5, 2.1, 2.2 |
| `everything-claude-code:deployment-patterns` | 2.4 |

---

## Pending (Future — not in current scope)

These were explicitly deferred. Add to a future phase when ready.

| Feature | Notes |
|---------|-------|
| X/Twitter integration | Requires paid API (~$100/mo). Add when budget allows. |
| LinkedIn integration | No public API. Needs third-party scraper service (e.g. Apify). |
| Google Scholar alerts | No official API. Needs third-party scraper or manual workaround. |
| Discord sources | Access-dependent. HF + EleutherAI announcement channels only. |
| Full-text search | Postgres `tsvector` or Meilisearch. Phase 2+. |
| Save for later / bookmarks | Phase 2+. Scoped to user account. |
| Email digest / newsletter | Out of scope for now. |
| Mobile native app | Out of scope for now. |
| Real-time push notifications | Out of scope for now. |
| Custom domain | Add after Phase 2.4 when app is stable. |

---

## Key Constraints

- **Curator, not archive** — never store full article content; only title, URL, excerpt, summary
- **Sources are config, not code** — adding/editing a source never requires a code deploy
- **No silent failures** — health monitor auto-flags broken sources
- **Source history is permanent** — retire sources, never delete
- **All LLM calls via LiteLLM** — never call provider SDKs directly; model controlled by env var
- **Cost control** — daily LLM cost cap enforced in code; exceeding it stops the job gracefully
- **No secrets in code** — all secrets in AWS Secrets Manager, injected as ECS task env vars
- **Mobile first** — every UI component built at 375px before any other breakpoint
