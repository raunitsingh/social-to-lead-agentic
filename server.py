"""
server.py
─────────────────────────────────────────────────────────────────────────────
Flask server — `python -m http.server 8080`

Serves:
  GET  /ui/index.html  → the chat UI
  POST /chat           → LangGraph agent → Supabase
  GET  /health         → status check

Run:
  python server.py

Then open: http://localhost:8080/ui/index.html
─────────────────────────────────────────────────────────────────────────────
"""

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import uuid
import os

load_dotenv()

app = Flask(__name__)

# ── Session store (thread_id per browser session) ────────────────────────────
# Key: session_id (string), Value: thread_id (LangGraph UUID)
_sessions: dict[str, str] = {}

def get_thread_id(session_id: str) -> str:
    if session_id not in _sessions:
        _sessions[session_id] = str(uuid.uuid4())
    return _sessions[session_id]


# ── Lazy-load the graph once ──────────────────────────────────────────────────
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        from agent.graph import graph
        _graph = graph
    return _graph


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return jsonify({"status": "ok", "ui": "/ui/index.html"})

@app.get("/health")
def health():
    return jsonify({"status": "healthy"})

@app.get("/ui/<path:filename>")
def serve_ui(filename):
    """Serve static UI files from the ui/ directory."""
    return send_from_directory("ui", filename)


@app.post("/chat")
def chat():
    """
    Main endpoint called by the UI on every message.

    Request:  { "message": "...", "session_id": "..." }
    Response: {
        "text":       "agent reply",
        "intent":     "high_intent",
        "name":       "John Doe" | null,
        "email":      "..." | null,
        "platform":   "YouTube" | null,
        "captured":   true | false,
        "leadCard":   { name, email, platform } | null
    }
    """
    data = request.get_json(silent=True) or {}
    message    = data.get("message", "").strip()
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not message:
        return jsonify({"error": "message required"}), 400

    thread_id = get_thread_id(session_id)
    config    = {"configurable": {"thread_id": thread_id}}

    try:
        graph  = get_graph()
        result = graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
    except Exception as e:
        return jsonify({"error": str(e), "text": "Sorry, something went wrong. Please try again."}), 500

    # ── Extract reply ─────────────────────────────────────────────────────────
    messages = result.get("messages", [])
    reply    = messages[-1].content if messages else "..."

    # ── Extract state for sidebar updates ────────────────────────────────────
    name      = result.get("collected_name")     or None
    email     = result.get("collected_email")    or None
    platform  = result.get("collected_platform") or None
    intent    = result.get("intent")             or None
    captured  = result.get("lead_captured",      False)

    # Clean up empty strings from qualify_node's "" sentinel
    if name     == "": name     = None
    if email    == "": email    = None
    if platform == "": platform = None

    # ── Build lead card payload when capture just happened ────────────────────
    lead_card = None
    if captured and name and email and platform:
        lead_card = {"name": name, "email": email, "platform": platform}

    return jsonify({
        "text":     reply,
        "intent":   intent,
        "name":     name,
        "email":    email,
        "platform": platform,
        "captured": captured,
        "leadCard": lead_card,
        "session_id": session_id,
    })


@app.delete("/session/<session_id>")
def reset_session(session_id: str):
    """Called by the UI's 'New Session' button to clear LangGraph memory."""
    _sessions.pop(session_id, None)
    return jsonify({"reset": session_id})


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"\n  AutoStream Agent server starting...")
    print(f"  UI  → http://localhost:{port}/ui/index.html")
    print(f"  API → http://localhost:{port}/chat\n")
    app.run(host="0.0.0.0", port=port, debug=False)