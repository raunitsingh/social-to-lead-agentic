from __future__ import annotations

import os
from datetime import datetime, timezone
from config import logger
from langgraph.checkpoint.memory import MemorySaver

# ── LangGraph checkpointer (unchanged) ───────────────────────────────────────
# Single shared instance — import this wherever the graph is compiled
checkpointer = MemorySaver()


# ── Supabase conversation logger (optional, additive) ─────────────────────────

_supabase = None


def _get_supabase():
    global _supabase
    if _supabase is not None:
        return _supabase

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        return None

    try:
        from supabase import create_client
        _supabase = create_client(url, key)
        return _supabase
    except Exception:
        return None


def log_message(
    session_id: str,
    role: str,          # "human" | "ai"
    content: str,
    intent: str | None = None,
) -> None:
    """
    Write one message to the conversations table.
    Silent no-op if Supabase is not configured — never raises.

    Call this from your graph nodes after each human/AI turn:

        from agent.memory import log_message
        log_message(thread_id, "human", user_text, state["intent"])
        log_message(thread_id, "ai",    ai_reply,  state["intent"])
    """
    client = _get_supabase()
    if client is None:
        return

    payload = {
        "session_id": session_id,
        "role":       role,
        "content":    content,
        "intent":     intent,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        client.table("conversations").insert(payload).execute()
    except Exception as e:
        logger.error(f"Failed to log message to Supabase: {e}")


def get_conversation_history(session_id: str) -> list[dict]:
    """
    Fetch all messages for a session from Supabase, ordered by time.
    Returns [] if Supabase is not configured or on error.

    Useful for the UI sidebar or analytics — not used by the graph itself.
    """
    client = _get_supabase()
    if client is None:
        return []

    try:
        result = (
            client.table("conversations")
            .select("role, content, intent, created_at")
            .eq("session_id", session_id)
            .order("created_at")
            .execute()
        )
        return result.data or []
    except Exception as e:
        logger.error(f"Failed to fetch conversation history: {e}")
        return []