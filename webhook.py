"""
webhook.py — Production FastAPI Server
Serves static HTML UI + LangGraph chat API
Runs: uvicorn webhook:app --host 0.0.0.0 --port $PORT
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import uuid
import os
from pathlib import Path

load_dotenv()

app = FastAPI(title="AutoStream Agent")

# ── CORS for development & production ─────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Session store (thread_id per browser session) ────────────────────────
_sessions: dict[str, str] = {}

def get_thread_id(session_id: str) -> str:
    if session_id not in _sessions:
        _sessions[session_id] = str(uuid.uuid4())
    return _sessions[session_id]


# ── Lazy-load the graph once ─────────────────────────────────────────────
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        from agent.graph import graph
        _graph = graph
    return _graph


# ── Routes ───────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@app.post("/chat")
def chat(data: dict):
    """
    Main chat endpoint — processes messages through LangGraph agent.
    
    Request:  { "message": "...", "session_id": "..." }
    Response: {
        "text":       "agent reply",
        "intent":     "high_intent",
        "name":       "John Doe" | null,
        "email":      "..." | null,
        "platform":   "YouTube" | null,
        "captured":   true | false,
        "leadCard":   { name, email, platform } | null,
        "session_id": "..."
    }
    """
    message    = data.get("message", "").strip()
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not message:
        return {"error": "message required", "status": 400}

    thread_id = get_thread_id(session_id)
    config    = {"configurable": {"thread_id": thread_id}}

    try:
        graph  = get_graph()
        result = graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
    except Exception as e:
        return {"error": str(e), "text": "Sorry, something went wrong. Please try again.", "status": 500}

    # ── Extract reply ─────────────────────────────────────────────────────
    messages = result.get("messages", [])
    reply    = messages[-1].content if messages else "..."

    # ── Extract state for sidebar updates ─────────────────────────────────
    name      = result.get("collected_name")     or None
    email     = result.get("collected_email")    or None
    platform  = result.get("collected_platform") or None
    intent    = result.get("intent")             or None
    captured  = result.get("lead_captured",      False)

    # Clean up empty strings from qualify_node's "" sentinel
    if name     == "": name     = None
    if email    == "": email    = None
    if platform == "": platform = None

    # ── Build lead card payload when capture just happened ────────────────
    lead_card = None
    if captured and name and email and platform:
        lead_card = {"name": name, "email": email, "platform": platform}

    return {
        "text":     reply,
        "intent":   intent,
        "name":     name,
        "email":    email,
        "platform": platform,
        "captured": captured,
        "leadCard": lead_card,
        "session_id": session_id,
    }


@app.delete("/session/{session_id}")
def reset_session(session_id: str):
    """Reset a session's LangGraph memory."""
    _sessions.pop(session_id, None)
    return {"reset": session_id}


# ── Serve static UI ──────────────────────────────────────────────────────
# Mount static files for /ui/* routes
app.mount("/ui", StaticFiles(directory="ui"), name="ui")


# ── Root route — serve index.html ────────────────────────────────────────
@app.get("/")
async def root():
    """Serve UI at root."""
    ui_path = Path("ui/index.html")
    if ui_path.exists():
        return FileResponse(ui_path, media_type="text/html")
    return {"error": "UI not found", "status": 404}
