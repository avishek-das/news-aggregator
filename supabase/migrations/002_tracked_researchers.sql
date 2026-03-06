-- Migration 002: tracked_researchers table
-- Run after 001_initial_schema.sql

CREATE TABLE IF NOT EXISTS tracked_researchers (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name          text NOT NULL,
  affiliation   text,
  homepage_url  text,
  identifiers   jsonb NOT NULL DEFAULT '{}',
  -- e.g. {"semantic_scholar_id": "...", "twitter_handle": "..."}
  created_at    timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_tracked_researchers_name
  ON tracked_researchers (name);
