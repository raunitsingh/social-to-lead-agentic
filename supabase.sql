-- ─────────────────────────────────────────────────────────────────────────
--  AutoStream Agent — Supabase Schema
--  Run this once in your Supabase project → SQL Editor → New query
-- ─────────────────────────────────────────────────────────────────────────

-- 1. LEADS TABLE
--    One row per captured lead. Written by save_lead_to_supabase().
-- ─────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS leads (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  text,
    name        text        NOT NULL,
    email       text        NOT NULL,
    platform    text        NOT NULL,
    captured_at timestamptz DEFAULT now(),
    source      text        DEFAULT 'autostream-agent'
);

-- 2. CONVERSATIONS TABLE
--    One row per message turn. Written by log_message().
-- ─────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  text        NOT NULL,
    role        text        NOT NULL CHECK (role IN ('human', 'ai')),
    content     text        NOT NULL,
    intent      text,
    created_at  timestamptz DEFAULT now()
);

-- Index for fast per-session lookups
CREATE INDEX IF NOT EXISTS idx_conversations_session
    ON conversations (session_id, created_at);

-- 3. DISABLE Row Level Security for service key access
--    (Service key bypasses RLS anyway, but being explicit is good practice)
ALTER TABLE leads         ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Allow service role full access
CREATE POLICY "service role full access leads"
    ON leads FOR ALL
    TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "service role full access conversations"
    ON conversations FOR ALL
    TO service_role USING (true) WITH CHECK (true);

-- ─────────────────────────────────────────────────────────────────────────
--  Useful queries for monitoring
-- ─────────────────────────────────────────────────────────────────────────

-- View all leads
-- SELECT * FROM leads ORDER BY captured_at DESC;

-- View a specific session's conversation
-- SELECT role, content, intent, created_at
-- FROM conversations
-- WHERE session_id = 'your-session-uuid'
-- ORDER BY created_at;

-- Count leads per platform
-- SELECT platform, COUNT(*) FROM leads GROUP BY platform;