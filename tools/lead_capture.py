from __future__ import annotations

import os
from datetime import datetime, timezone
from config import logger


# ── Supabase client (lazy-loaded, optional) ───────────────────────────────────

_supabase = None

def _get_supabase():
    """
    Returns a Supabase client, or None if credentials are not configured.
    Lazy-loaded so the rest of the app works without supabase-py installed.
    """
    global _supabase
    if _supabase is not None:
        return _supabase

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")   # use service key (bypasses RLS)

    if not url or not key:
        logger.warning(
            "Supabase credentials not set — leads will NOT be persisted to DB. "
            "Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env to enable."
        )
        return None

    try:
        from supabase import create_client
        _supabase = create_client(url, key)
        logger.info("Supabase client initialised ✓")
        return _supabase
    except ImportError:
        logger.warning("supabase package not installed — run: pip install supabase")
        return None
    except Exception as e:
        logger.error(f"Supabase init failed: {e}")
        return None


# ── Core functions ────────────────────────────────────────────────────────────

def mock_lead_capture(name: str, email: str, platform: str) -> None:
    """
    Simulates sending lead data to a CRM backend.
    Only called from capture_node after all 3 fields are confirmed.
    Original assignment requirement — kept exactly as specified.
    """
    logger.info(f"LEAD CAPTURED → name={name}, email={email}, platform={platform}")
    print(f"\n{'='*55}")
    print(f"  ✅ Lead captured successfully!")
    print(f"     Name     : {name}")
    print(f"     Email    : {email}")
    print(f"     Platform : {platform}")
    print(f"{'='*55}\n")


def save_lead_to_supabase(
    name: str,
    email: str,
    platform: str,
    session_id: str | None = None,
) -> bool:
    """
    Persists a captured lead to the Supabase 'leads' table.

    Returns True on success, False on failure (never raises — agent
    should not crash because of a DB write).

    Table schema (create this in Supabase SQL editor):

        CREATE TABLE leads (
            id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id  text,
            name        text NOT NULL,
            email       text NOT NULL,
            platform    text NOT NULL,
            captured_at timestamptz DEFAULT now(),
            source      text DEFAULT 'autostream-agent'
        );
    """
    client = _get_supabase()
    if client is None:
        return False

    payload = {
        "session_id":  session_id,
        "name":        name,
        "email":       email,
        "platform":    platform,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source":      "autostream-agent",
    }

    try:
        result = client.table("leads").insert(payload).execute()
        logger.info(f"Lead saved to Supabase ✓  id={result.data[0].get('id')}")
        return True
    except Exception as e:
        logger.error(f"Failed to save lead to Supabase: {e}")
        return False


def capture_lead(
    name: str,
    email: str,
    platform: str,
    session_id: str | None = None,
) -> None:
    """
    Single entry point called by capture_node in graph.py.

    Runs both the terminal print (assignment requirement) and
    the Supabase persist (production layer) together.
    """
    # Step 1: original assignment requirement
    mock_lead_capture(name, email, platform)

    # Step 2: persist to DB (silent fail if Supabase not configured)
    saved = save_lead_to_supabase(name, email, platform, session_id)
    if saved:
        print(f"  📦 Lead also saved to Supabase database.\n")