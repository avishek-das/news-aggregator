# AI News Aggregator — Ideas v2

## Problem Statement

The AI field evolves at an overwhelming pace — new research papers, models, products, and GitHub repos drop weekly. Missing even two weeks of updates feels like falling behind. No single platform covers everything: relevant content is scattered across X, LinkedIn, arXiv, Reddit, conference sites, and company blogs.

The deeper problem is **noise**. Going to X to find one important AI update means wading through an endless feed of unrelated content. Going to LinkedIn to read one insightful post means getting pulled into notifications and distractions. These platforms are not designed for focused discovery — they are designed to keep you on them as long as possible.

The goal is not to replace these platforms. It is to **eliminate the need to visit them for discovery**. This tool tells you exactly what to read. You go, read the one thing, and come back. Nothing more.

**Goal:** A single, distraction-free website that surfaces only what matters in AI — personally relevant, pre-filtered, and ready to read — so you never have to open X or LinkedIn just to stay current.

---

## Content Sources to Track

### Research Preprints

**arXiv** — `arxiv.org`
New preprints in the following subject areas, tracked via daily listing feeds:

- `cs.AI` — Artificial Intelligence → `arxiv.org/list/cs.AI`
- `cs.LG` — Machine Learning → `arxiv.org/list/cs.LG`
- `cs.CL` — Computation and Language (NLP) → `arxiv.org/list/cs.CL`
- `cs.CV` — Computer Vision → `arxiv.org/list/cs.CV`
- `stat.ML` — Statistics / Machine Learning → `arxiv.org/list/stat.ML`

**Semantic Scholar** — `semanticscholar.org`

- Highly cited new papers
- Trending papers (by citation velocity)

**Google Scholar** — `scholar.google.com`

- Citation alerts for tracked key authors
- New papers in tracked topics

### Code & Benchmarks

**Papers with Code** — `paperswithcode.com`

- New papers with released code
- State-of-the-art benchmark leaderboards

### Conference Proceedings

Accepted papers at top venues (tracked when proceedings are published):

| Conference | Full Name                                                       | Domain        |
| ---------- | --------------------------------------------------------------- | ------------- |
| ICML       | International Conference on Machine Learning                    | ML            |
| NeurIPS    | Conference on Neural Information Processing Systems             | ML / AI       |
| ICLR       | International Conference on Learning Representations            | Deep Learning |
| CVPR       | Conference on Computer Vision and Pattern Recognition           | Vision        |
| ECCV       | European Conference on Computer Vision                          | Vision        |
| ACL        | Annual Meeting of the Association for Computational Linguistics | NLP           |
| EMNLP      | Empirical Methods in Natural Language Processing                | NLP           |
| AAAI       | AAAI Conference on Artificial Intelligence                      | AI            |
| IJCAI      | International Joint Conference on AI                            | AI            |
| COLM       | Conference on Language Modeling                                 | LLMs          |

### Under Review & Pre-Publication

**OpenReview** — `openreview.net`

- Submissions currently under review at tracked venues
- Reviews and scores made public during open review periods
- Papers that receive high reviewer scores before acceptance decisions

### People & Organizations

- Top AI researchers (tracked as individuals across all sources above)
- Companies: OpenAI, Anthropic, Google DeepMind, Meta AI, Mistral, etc.

### Social Media & Communities

**X (Twitter)** — `x.com`

- Posts from tracked researchers, company accounts, and curated AI lists
- Replies and threads from tracked accounts (not the full firehose)
- Tracked via curated lists or account-level monitoring, not keyword search

**LinkedIn** — `linkedin.com`

- AI-related posts from tracked researchers and company pages
- Lab announcements and research highlights from followed accounts

**Reddit** — `reddit.com`

- r/MachineLearning
- r/LocalLLaMA
- r/artificial
- r/deeplearning
- r/ChatGPT

**Hacker News** — `news.ycombinator.com`

- AI/ML stories that reach the front page
- High-comment threads about AI topics (signal of community interest)

**Lobsters** — `lobste.rs`

- Stories tagged `machine-learning`, `ai`, `nlp`, `llm`

**Discord** _(best-effort, access-dependent)_

- Key AI community servers where public announcements are made
- Lab-run servers (e.g. Hugging Face, EleutherAI) — announcement channels only
- Feasibility depends on API access; lower priority source

### Open Source & Code

**GitHub Trending** — `github.com/trending`

- Daily and weekly trending repositories
- Filtered by language: Python, TypeScript
- Filtered by topic: machine-learning, deep-learning, AI

**GitHub Releases** — `github.com` (via API / RSS)

- New releases from explicitly tracked repositories
- Release notes and changelogs from starred/followed repos

**GitHub Topics** — `github.com/topics`

- Repos tagged: `machine-learning`, `deep-learning`, `llm`, `large-language-models`, `generative-ai`, `transformers`, `diffusion-models`

**Hugging Face** — `huggingface.co`

- New model uploads and model cards
- New datasets
- New Spaces (demos)
- Trending models and datasets (daily)

**PyPI** — `pypi.org`

- New releases of tracked ML/AI packages (e.g. `transformers`, `torch`, `langchain`, `llama-index`, etc.)

### Models & Benchmarks

**Hugging Face Open LLM Leaderboard** — `huggingface.co/spaces/open-llm-leaderboard`

- New model entries and ratings
- SOTA changes and ranking shifts

**LM Arena / Chatbot Arena** — `lmarena.ai`

- Crowd-sourced model rankings (Elo ratings)
- New battle results and ranking updates

**Model Releases from Labs**

- Model cards and announcements from tracked labs (see Companies & Labs below)
- New weights, APIs, and fine-tune releases

**AI Benchmarks** — tracked results across:
| Benchmark | What It Measures |
|---|---|
| MMLU | Multitask language understanding |
| HumanEval | Code generation |
| MATH | Mathematical reasoning |
| ARC | Abstract reasoning |
| HellaSwag | Commonsense reasoning |
| New benchmarks as they emerge |

### Companies & Labs

Tracked via official blogs, release pages, and social accounts:

| Lab                | Focus                          |
| ------------------ | ------------------------------ |
| OpenAI             | GPT series, Sora, APIs         |
| Anthropic          | Claude series                  |
| Google DeepMind    | Gemini, research               |
| Meta AI            | LLaMA, open-source research    |
| Microsoft Research | Applied AI, Azure AI           |
| Apple ML           | On-device ML, research blog    |
| Mistral AI         | Open-weight models             |
| Cohere             | Enterprise NLP, Command series |
| xAI                | Grok series                    |
| Emerging startups  | Tracked as they gain traction  |

### Products & Tools

**Product Hunt** — `producthunt.com`

- New AI product launches (daily top products filtered to AI category)
- Newly launched AI tools and apps

**AI Tool Directories**

- There's An AI For That — `theresanaiforthat.com`
- Futurepedia — `futurepedia.io`
- New tool listings and category updates across directories

**App Stories**

- New or significantly updated AI apps (mobile and web)
- Notable feature launches from existing AI products

**API Changelogs** — tracked from official sources:

- OpenAI API changelog — `platform.openai.com/docs/changelog`
- Anthropic API changelog — `docs.anthropic.com/changelog`
- Google AI (Gemini API) changelog — `ai.google.dev`

### Podcasts & Video

**YouTube Channels** _(initial seed list — to be expanded dynamically)_

- Andrej Karpathy
- Yannic Kilcher
- Two Minute Papers
- AI Explained
- Lex Fridman (AI episodes)
- Lab-official channels: OpenAI, Google DeepMind, Meta AI

**Podcasts** _(initial seed list — to be expanded dynamically)_

- Lex Fridman Podcast
- The TWIML AI Podcast
- Practical AI
- Latent Space
- No Priors

**Conference Talks**

- Recorded keynotes and talks from tracked conferences (ICML, NeurIPS, ICLR, CVPR, etc.)
- Surfaced when recordings are published post-conference

---

## Source Management

**Sources are not a static list.** The source registry is a living database — managed through a simple UI or config, never a code deployment.

### Adding & Editing Sources

A simple admin UI (or config file for early versions) allows:

- Register a new source with name, URL, category, type, and priority
- Edit any source field — URL changes, rename, recategorize
- Change priority (affects fetch frequency — see below)
- Update tracking parameters (e.g. which RSS feed path, which subreddit, which GitHub topic tag)
- All changes take effect on the next fetch cycle — no restart required

### Source Lifecycle

Sources are never hard-deleted. Instead:

| State        | Meaning                                                |
| ------------ | ------------------------------------------------------ |
| **Active**   | Fetched on schedule, items appear in feed              |
| **Inactive** | Paused — no new fetches, history preserved             |
| **Flagged**  | Health check failed — needs review before reactivating |

- Retiring a source marks it inactive, preserving all historical items it contributed
- Inactive sources can be reactivated at any time and resume fetching immediately
- History is always kept — items already ingested remain searchable and visible

### Source Health Monitoring

The system automatically monitors each source and flags it when:

- Fetch returns no new items for an unexpected duration (e.g. 3 consecutive days for a daily source)
- HTTP errors, timeouts, or auth failures occur repeatedly
- Feed format changes and parsing breaks

Flagged sources appear in a health dashboard with:

- Last successful fetch timestamp
- Error type and message
- Suggested action (check URL, update parser, contact source)

Alerts surface in the admin UI — no silent failures.

### Priority-Based Fetch Scheduling

Each source has a priority level that controls how often it is checked:

| Priority   | Fetch Frequency     | Example Sources                                              |
| ---------- | ------------------- | ------------------------------------------------------------ |
| **High**   | Every 2–4 hours     | arXiv daily listings, HN front page, tracked lab blogs       |
| **Medium** | Once or twice a day | Reddit top posts, GitHub trending, Hugging Face new models   |
| **Low**    | Every 2–3 days      | Conference proceedings, PyPI package releases, podcast feeds |

- Priority can be changed at any time from the source management UI
- High-priority sources consume more fetch budget — useful to keep the count of high-priority sources small and deliberate
- Fetch scheduling respects rate limits and API quotas per source

---

## Data Approach

This website is a **curator, not an archive**. It does not scrape or store full article content.

The core job is two things:

1. **Discover** — continuously find relevant new content across all tracked sources, then curate, rank, and filter it based on topic relevance and user preference signals.
2. **Link** — for each item, show a title, a short summary, source attribution, and a direct link to the original. The user reads on the original platform.

This approach is intentional:

- No copyright or scraping issues
- No storage of content that changes or gets deleted upstream
- The value is in the **curation and filtering**, not in re-hosting content
- The website eliminates the need to _browse_ noisy platforms for discovery — it tells you exactly what is worth reading and sends you straight there

What gets stored: title, URL, source, publish date, a brief excerpt or AI-generated summary, category tags, and user feedback signals. Nothing more.

---

## Product Roadmap

The product is built in **two major phases**, each broken into sub-phases. Every sub-phase follows the same loop:

```
Plan → Build → Test → Review → Gate check → next sub-phase
```

No sub-phase starts without a confirmed plan. No sub-phase ends without passing its gate. This ensures every increment is working software — not half-built features waiting to be integrated later.

---

### How the Build Loop Works

Each sub-phase follows this exact sequence:

1. **Plan** — run `planner` + `architect` agents, produce task list and design notes, confirm before writing any code
2. **Build** — implement the smallest thing that satisfies the sub-phase goal, following TDD (write test first, then code)
3. **Test** — unit tests, integration tests, and E2E for critical flows; must hit 80%+ coverage
4. **Review** — `code-reviewer` agent checks all changes; `security-reviewer` for anything touching data or APIs
5. **Gate check** — manually verify the gate criteria are met before proceeding
6. **Reflect** — note anything that felt wrong, any shortcuts taken, any tech debt created; decide whether to address it now or log it

If a gate is not met, the sub-phase is not done. Fix it before moving forward.

---

### Phase 1 — Personal Feed (Single-User)

> Goal: A working personal dashboard for one user, no auth required. Each sub-phase produces something you can actually open in a browser and use.

---

#### 1.1 — Foundation

**What we're building:** Project skeleton, CI, database, and the basic data model. Nothing visible yet — just a solid base.

| Step | Task | Test |
|---|---|---|
| 1 | Confirm tech stack via `architect` agent | ADR written and approved |
| 2 | Scaffold project (Next.js + Tailwind + Postgres) | `npm run build` passes |
| 3 | Set up CI pipeline (lint + type-check + test on every push) | CI green on empty commit |
| 4 | Define DB schema: `sources`, `items`, `categories` | Migration runs cleanly, rollback tested |
| 5 | Seed DB with 2–3 test sources | Query returns seeded rows |

**Gate:** Project builds. CI is green. DB schema is migrated and tested. `architect` has signed off on tech stack choices.

---

#### 1.2 — First Data: Two Sources Live

**What we're building:** Real data flowing in from two sources (arXiv + Hacker News). No UI yet — verify via DB or simple JSON endpoint.

| Step | Task | Test |
|---|---|---|
| 1 | arXiv RSS adapter — fetch `cs.AI` daily listing, parse, store items | Unit test: parse fixture RSS → correct item shape |
| 2 | Hacker News adapter — fetch front page, filter AI stories | Unit test: mock API response → filtered items |
| 3 | Background job: runs both adapters on a schedule | Integration test: job runs, items appear in DB |
| 4 | Deduplication: same URL from two runs is stored once | Unit test: insert duplicate → only one row |
| 5 | `/api/items` endpoint returns stored items as JSON | Integration test: GET → 200, items array |

**Gate:** arXiv and HN are fetching live data. Items are in the DB. Deduplication works. 80%+ test coverage on ingestion code. `code-reviewer` has signed off.

---

#### 1.3 — First UI: Feed on Screen

**What we're building:** A real, usable feed page. Open it on your phone — it should feel like a product.

| Step | Task | Test |
|---|---|---|
| 1 | Feed page: list of item cards (title, source badge, date, excerpt) | E2E: page loads, cards visible |
| 2 | Mobile layout: single column, bottom nav bar, 375px viewport | Visual check on real device |
| 3 | Desktop layout: sidebar + feed column, 1280px viewport | Visual check in browser |
| 4 | Dark / light mode (follows system preference) | Toggle works, no flash on load |
| 5 | Skeleton loaders while data is fetching | E2E: skeletons appear before cards |
| 6 | Clicking a card opens the original URL in a new tab | E2E: click → correct URL opened |

**Gate:** Feed loads live data on mobile and desktop. Looks good on a real phone. All E2E tests pass. No horizontal scroll at any breakpoint.

---

#### 1.4 — Source Expansion: All Major Sources

**What we're building:** All remaining sources wired up. Source management UI so sources can be toggled without touching code.

| Step | Task | Test |
|---|---|---|
| 1 | Add adapters: Reddit, GitHub Trending, Papers with Code, Hugging Face | Integration test per adapter |
| 2 | Add adapters: arXiv remaining feeds (cs.LG, cs.CL, cs.CV, stat.ML) | Integration test: each feed returns items |
| 3 | Category tagging per item (research / code / community / product) | Unit test: item from arXiv → tagged "research" |
| 4 | Category filter tabs in feed UI | E2E: select "code" tab → only code items visible |
| 5 | Source management page: list sources, toggle active/inactive | E2E: disable a source → its items disappear from feed |
| 6 | Regression test: all previously passing tests still pass | CI green |

**Gate:** All sources ingesting. Filters work. Source toggle works without code deploy. No regressions. Each new adapter has integration test coverage.

---

#### 1.5 — Source Management: Full CRUD

**What we're building:** Complete source admin — add, edit, change priority, retire. Health monitoring.

| Step | Task | Test |
|---|---|---|
| 1 | Add source form: name, URL, type, category, priority | E2E: submit form → source appears in list, starts fetching |
| 2 | Edit source: update any field, takes effect next fetch cycle | Integration test: edit URL → next fetch uses new URL |
| 3 | Retire source: marks inactive, history preserved | E2E: retire → items still visible, no new fetches |
| 4 | Reactivate source: resumes fetching immediately | Integration test: reactivate → next scheduled fetch runs |
| 5 | Health monitor: flag source after 3 consecutive empty/error fetches | Unit test: 3 failures → status = "flagged" |
| 6 | Health dashboard: show flagged sources with last error and timestamp | E2E: flagged source appears in dashboard with error detail |

**Gate:** Full source CRUD works in UI. Health monitoring flags broken sources. History preserved on retire. All E2E and integration tests pass.

---

#### 1.6 — AI Summarization

**What we're building:** Claude-generated summaries on item cards. Cost-controlled, batched overnight.

| Step | Task | Test |
|---|---|---|
| 1 | Summarization pipeline: takes item excerpt → returns 2–3 sentence summary | Unit test: mock Claude API → correct summary stored |
| 2 | Batch job: summarize unsummarized items nightly (not on demand) | Integration test: job runs → items get summaries |
| 3 | Cost guard: cap daily Claude API spend, log token usage | Unit test: token count exceeds cap → job stops gracefully |
| 4 | Fallback: show raw excerpt if summary unavailable | E2E: item without summary → excerpt shown, no blank card |
| 5 | Expandable summary on card (collapsed by default) | E2E: tap "show summary" → summary expands |
| 6 | Security review on API key handling | `security-reviewer` agent sign-off |

**Gate:** Summaries appear on live cards. Batch job runs on schedule. Daily cost is within budget. No API keys in code. Security reviewer has signed off.

---

### Phase 2 — Multi-User Platform

> Goal: Open the platform beyond a single user. Each person has their own feed, preferences, and feedback history. Phase 2 does not start until Phase 1 is stable and you are actively using it.

---

#### 2.1 — Personalization & Feedback

**What we're building:** Thumbs up/down on items. Feed starts learning from your signals.

| Step | Task | Test |
|---|---|---|
| 1 | Feedback schema: `item_feedback` table (item_id, signal, timestamp) | Migration tested, rollback verified |
| 2 | Thumbs up / down buttons on desktop cards | E2E: click thumbs up → feedback stored in DB |
| 3 | Swipe right (👍) / swipe left (dismiss) on mobile | E2E: swipe gesture → correct signal recorded |
| 4 | Feed ranking: items from liked sources/topics score higher | Unit test: ranking function re-orders items correctly |
| 5 | Feed visibly changes after 5+ interactions | Manual check: like 5 research papers → research items rise |

**Gate:** Feedback persists. Feed ranking changes based on signals. Swipe works on mobile. Unit tests cover ranking logic.

---

#### 2.2 — User Authentication

**What we're building:** Sign-up, sign-in, sign-out. All pages protected.

| Step | Task | Test |
|---|---|---|
| 1 | Confirm auth strategy via `architect` (magic link vs OAuth vs email+password) | ADR written |
| 2 | Sign-up and sign-in flows | E2E: full sign-up flow → lands on feed |
| 3 | Sign-out | E2E: sign-out → redirected to login |
| 4 | Route protection: unauthenticated requests redirect to login | Integration test: GET /feed without session → 302 |
| 5 | Session management and secure token storage | `security-reviewer` agent mandatory sign-off |

**Gate:** Full auth flow works end-to-end. All routes protected. Security reviewer passes. No secrets in code.

---

#### 2.3 — Per-User Data

**What we're building:** Each user's feedback and preferences are isolated. Settings page to manage sources and topics.

| Step | Task | Test |
|---|---|---|
| 1 | Scope all feedback and preferences to `user_id` | Integration test: two users, independent feedback |
| 2 | Migrate existing single-user data to user-scoped schema | Migration script tested: data preserved, no loss |
| 3 | Settings page: toggle sources, manage tracked topics and people | E2E: disable source in settings → disappears from feed |
| 4 | Row-level security (RLS) on all user-scoped tables | Integration test: user A cannot read user B's feedback |

**Gate:** Two test accounts have completely independent, diverging feeds. RLS verified. Data migration tested.

---

#### 2.4 — Production Hardening

**What we're building:** Stable, monitored, production-ready deployment.

| Step | Task | Test |
|---|---|---|
| 1 | Deployment pipeline: dev → staging → production | Staging deploy succeeds before any prod deploy |
| 2 | All secrets in environment variables, none in code | Security scan: grep for hardcoded keys → zero results |
| 3 | Rate limiting on all API endpoints | Integration test: exceed limit → 429 returned |
| 4 | Error monitoring (Sentry or equivalent) | Trigger a test error → appears in dashboard |
| 5 | Performance budget: feed loads under 2s on mobile (3G throttle) | Lighthouse / WebPageTest score verified |
| 6 | Full verification loop before prod release | Build + types + lint + tests + security scan all pass |

**Gate:** Staging works end-to-end. All verification checks green. Performance budget met. Staged rollout to production.

---

## UI / UX Requirements

### Design Philosophy

- **Mobile-first:** Primary design target is mobile — laptop experience is an enhancement, not the baseline
- **Modern aesthetic:** Clean, minimal, content-forward design (think Linear, Vercel dashboard, or Perplexity)
- **High readability:** Typography and spacing optimized for reading articles and summaries on small screens

### Responsive Behavior

| Screen                      | Expected Experience                                          |
| --------------------------- | ------------------------------------------------------------ |
| Mobile (< 640px)            | Single-column feed, large tap targets, bottom navigation bar |
| Tablet (640–1024px)         | Two-column layout, sidebar optional                          |
| Laptop / Desktop (> 1024px) | Multi-column layout, persistent sidebar, keyboard shortcuts  |

### Mobile-Specific Requirements

- Bottom navigation bar (not hamburger menu) for primary sections
- Swipe gestures for feedback (swipe right = thumbs up, swipe left = dismiss)
- Fast load times — aggressive lazy loading and pagination
- Offline-friendly: cache last-viewed feed for no-connection scenarios
- Large, thumb-friendly tap targets (minimum 44px)
- No horizontal scrolling at any breakpoint

### Visual Design Targets

- Dark mode + light mode support (respects system preference by default)
- Smooth animations and micro-interactions (but not at the cost of performance)
- Card-based content layout with clear visual hierarchy
- Skeleton loaders instead of spinners for perceived performance

---

## Skills & Sub-Agents Plan

These are the specialized skills and sub-agents to set up before or during development to enforce quality and velocity.

### Skills to Use

| Skill                                            | When to Apply                                       |
| ------------------------------------------------ | --------------------------------------------------- |
| `frontend-patterns`                              | All React/Next.js component and state work          |
| `everything-claude-code:tdd`                     | Every feature — tests before implementation         |
| `everything-claude-code:api-design`              | Designing aggregation and preference APIs           |
| `everything-claude-code:security-review`         | Before any auth or data-persistence work            |
| `everything-claude-code:e2e`                     | Critical user flows (feed load, feedback, settings) |
| `everything-claude-code:deployment-patterns`     | CI/CD pipeline and production setup                 |
| `everything-claude-code:backend-patterns`        | API routes, data fetching, caching layers           |
| `everything-claude-code:database-migrations`     | Schema changes as features evolve                   |
| `everything-claude-code:postgres-patterns`       | Query optimization once DB is in use                |
| `everything-claude-code:cost-aware-llm-pipeline` | AI summarization and content ranking calls          |

### Sub-Agents to Configure

| Agent                  | Role                                                                        |
| ---------------------- | --------------------------------------------------------------------------- |
| `planner`              | Kick off each phase with a full implementation plan before coding           |
| `architect`            | Validate system design decisions (aggregation pipeline, caching, DB schema) |
| `tdd-guide`            | Enforce write-tests-first discipline on every feature                       |
| `code-reviewer`        | Review all PRs before merge                                                 |
| `security-reviewer`    | Review auth, API keys, and any user data handling                           |
| `e2e-runner`           | Run Playwright flows against dev and staging environments                   |
| `build-error-resolver` | Unblock failed builds quickly                                               |

### Agent Workflow Per Phase

```
Phase kick-off  →  planner + architect (parallel)
Feature build   →  tdd-guide → code-reviewer → security-reviewer
Pre-release     →  e2e-runner → deployment-patterns skill
```

---

## Development Principles

### Rule 1: Plan Before Any Code

Every sub-phase starts with `planner` + `architect` agents producing:

- Requirements restatement
- System/component design
- Risk assessment (HIGH / MEDIUM / LOW)
- Task breakdown

**No code is written until the plan is confirmed.**

### Rule 2: Test-Driven Development (TDD)

Every feature follows RED → GREEN → REFACTOR:

1. Write the test first (it fails)
2. Write minimal code to pass the test
3. Refactor without breaking the test
4. Verify 80%+ coverage before moving on

Use `tdd-guide` agent for every new feature and bug fix.

### Rule 3: Verification Before Merge

Before each sub-phase gate is cleared, run the full verification loop:

```
Build → Type Check → Lint → Tests (80%+ coverage) → Security Scan → Diff Review
```

### Rule 4: Small Iterations, Real Feedback

- Each sub-phase produces something usable and testable
- If a sub-phase output feels wrong, stop and course-correct before proceeding
- No "big bang" releases — every gate is a shippable checkpoint

### Rule 5: Security Is Not Optional

- `security-reviewer` agent runs before every sub-phase gate involving auth, APIs, or user data
- No hardcoded secrets — ever
- Rate limiting on all endpoints from day one

### Rule 6: Mobile Is the Primary Target

- Every UI component is built mobile-first
- Test on real mobile viewport (375px) before marking any UI task done
- E2E tests include mobile viewport simulation

---

## Open Questions (to resolve during planning)

### Data & Ingestion

| Question | Options | Notes |
|---|---|---|
| Default fetch frequency for high-priority sources | Every 2h / Every 4h / Configurable per source | Balance freshness vs. API rate limits |
| Deduplication strategy | URL fingerprint / title hash / content hash | Cross-source duplicates are common |
| How to handle paywalled sources | Skip / Show title only / Flag as paywalled | Affects LinkedIn, some journals |
| arXiv fetch method | RSS daily digest / API / HTML scrape | RSS is simplest and most stable |
| Google Scholar tracking | Manual alert setup / API (limited) / Scrape | No official API — may need workaround |

### AI & Summarization

| Question | Options | Notes |
|---|---|---|
| Summarization model | Claude Haiku (cost) / Sonnet (quality) / Both | Haiku for bulk, Sonnet for flagged items |
| When to summarize | On ingest (batch overnight) / On first view / On demand | Overnight batch preferred for cost control |
| Summary length | 2–3 sentences / 5 sentences / Configurable | Shorter is better on mobile |
| Relevance scoring | LLM-based / keyword match / embedding similarity | To be decided during architecture phase |

### Feed & Personalization

| Question | Options | Notes |
|---|---|---|
| Default feed sort | Recency / Relevance score / Hybrid | Hybrid likely best — recency + quality |
| Feedback mechanism | Thumbs up/down / Star / Swipe gesture | Swipe on mobile, buttons on desktop |
| How quickly feed adapts to feedback | Immediate re-rank / Next session / After N signals | After ~5 signals is a reasonable threshold |
| Content categories shown by default | All / Research only / Configurable on first run | Onboarding flow needed |

### Infrastructure & Hosting

| Question | Options | Notes |
|---|---|---|
| Hosting platform | Vercel + managed DB / Railway / Self-hosted VPS | Vercel + Supabase easiest for Phase 1 |
| Database | Postgres (Supabase) / SQLite (local) / PlanetScale | Postgres recommended for Phase 2 scaling |
| Background job runner | Cron via Vercel / BullMQ / pg-cron / Inngest | Needs to be reliable for source fetching |
| Source credential storage | Env vars / Secrets manager / Encrypted DB column | Never plaintext — env vars minimum |

### Auth (Phase 2)

| Question | Options | Notes |
|---|---|---|
| Auth strategy | Magic link / OAuth (Google) / Email + password | Magic link simplest; OAuth easiest for users |
| Session management | JWT / Cookie-based / Supabase Auth | Supabase Auth covers this out of the box |
| Multi-user data isolation | Row-level security (RLS) / App-layer filtering | RLS in Postgres is the cleanest approach |

---

## Out of Scope (for now)

- Mobile app
- Email digest / newsletter
- Real-time push notifications
