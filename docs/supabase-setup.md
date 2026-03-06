# Supabase Setup Guide

Your Supabase project is already created:
- **Project URL:** https://obnlucnwlkijttmleukx.supabase.co
- **DB host:** db.obnlucnwlkijttmleukx.supabase.co

## Step 1: Get your API keys

1. Go to https://supabase.com/dashboard/project/obnlucnwlkijttmleukx/settings/api
2. Copy:
   - **URL** → `SUPABASE_URL`
   - **anon / public key** → `SUPABASE_ANON_KEY`
   - **service_role / secret key** → `SUPABASE_SERVICE_KEY` (keep this secret)

## Step 2: Get your DB password and connection string

1. Go to Settings → Database
2. Your direct connection string is:
   `postgresql://postgres:[YOUR-PASSWORD]@db.obnlucnwlkijttmleukx.supabase.co:5432/postgres`
3. Replace `[YOUR-PASSWORD]` with your database password (set when you created the project)
4. This is your `DATABASE_URL`

## Step 3: Create your local .env file

```bash
cp .env.example backend/.env
```
Fill in the real values from steps 1–2.

## Step 4: Store credentials in AWS Secrets Manager

```bash
aws secretsmanager put-secret-value \
  --secret-id news-aggregator/supabase-db-url \
  --secret-string "postgresql://postgres:YOUR_PASSWORD@db.obnlucnwlkijttmleukx.supabase.co:5432/postgres" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id news-aggregator/supabase-anon-key \
  --secret-string "YOUR_ANON_KEY" \
  --region us-east-1

aws secretsmanager put-secret-value \
  --secret-id news-aggregator/supabase-service-key \
  --secret-string "YOUR_SERVICE_KEY" \
  --region us-east-1
```

## Step 5: Run the database migration

**Against Supabase (production/staging):**
```bash
psql "postgresql://postgres:YOUR_PASSWORD@db.obnlucnwlkijttmleukx.supabase.co:5432/postgres" \
  -f supabase/migrations/001_initial_schema.sql
```

**Against local docker-compose postgres (development):**
```bash
docker-compose up -d postgres
psql "postgresql://postgres:postgres@localhost:5432/news_aggregator" \
  -f supabase/migrations/001_initial_schema.sql
psql "postgresql://postgres:postgres@localhost:5432/news_aggregator" \
  -f supabase/seed.sql
```

## Step 6: Verify

```bash
psql "YOUR_DATABASE_URL" -c "SELECT name, category, status FROM sources;"
# Should return 3 rows after seed
```
