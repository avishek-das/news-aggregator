-- Migration 001: Initial schema
-- Apply:   psql $DATABASE_URL -f supabase/migrations/001_initial_schema.sql
-- Rollback: psql $DATABASE_URL -f supabase/migrations/001_initial_schema_rollback.sql

CREATE TABLE IF NOT EXISTS sources (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  url text NOT NULL,
  type text NOT NULL CHECK (type IN ('rss', 'api', 'scrape')),
  category text NOT NULL CHECK (category IN ('research', 'code', 'community', 'product', 'media')),
  priority text NOT NULL DEFAULT 'medium'
    CHECK (priority IN ('high', 'medium', 'low')),
  status text NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'inactive', 'flagged')),
  fetch_config jsonb NOT NULL DEFAULT '{}',
  last_fetched_at timestamptz,
  last_error text,
  consecutive_failures int NOT NULL DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id uuid NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
  title text NOT NULL,
  url text NOT NULL UNIQUE,
  excerpt text,
  summary text,
  published_at timestamptz,
  category text NOT NULL CHECK (category IN ('research', 'code', 'community', 'product', 'media')),
  is_paywalled boolean NOT NULL DEFAULT false,
  raw_metadata jsonb NOT NULL DEFAULT '{}',
  updated_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now(),
  last_seen_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS read_items (
  session_id text NOT NULL REFERENCES user_sessions(session_id) ON DELETE CASCADE,
  item_id uuid NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  read_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (session_id, item_id)
);

CREATE TABLE IF NOT EXISTS job_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  job_name text NOT NULL,
  run_date date NOT NULL,
  items_processed int NOT NULL DEFAULT 0,
  tokens_used int NOT NULL DEFAULT 0,
  cost_usd numeric(10, 6) NOT NULL DEFAULT 0,
  status text NOT NULL DEFAULT 'running'
    CHECK (status IN ('running', 'completed', 'failed')),
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (job_name, run_date)
);

CREATE TABLE IF NOT EXISTS tracked_researchers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  identifiers jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Indexes required for feed query performance
CREATE INDEX IF NOT EXISTS idx_items_source_id ON items (source_id);
CREATE INDEX IF NOT EXISTS idx_items_category_published ON items (category, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_items_created_at ON items (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_status ON sources (status);
CREATE INDEX IF NOT EXISTS idx_read_items_session_id ON read_items (session_id);
