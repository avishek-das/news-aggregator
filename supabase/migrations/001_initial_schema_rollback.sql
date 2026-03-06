-- Rollback migration 001 — drops all tables in dependency order
DROP TABLE IF EXISTS read_items;
DROP TABLE IF EXISTS tracked_researchers;
DROP TABLE IF EXISTS job_runs;
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS sources;
