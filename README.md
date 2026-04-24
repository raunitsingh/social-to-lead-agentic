<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/LangGraph-Agentic-22C55E?style=for-the-badge&logoColor=white"/>
<img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F97316?style=for-the-badge&logoColor=white"/>
<img src="https://img.shields.io/badge/FAISS-RAG_Pipeline-8B5CF6?style=for-the-badge&logoColor=white"/>
<img src="https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
<img src="https://img.shields.io/badge/Netlify-Live_Demo-00C7B7?style=for-the-badge&logo=netlify&logoColor=white"/>

<br/><br/>

# 🎬 AutoStream — Conversational AI Sales Agent

### Social-to-Lead Agentic Workflow · ServiceHive × Inflx · ML Internship Assignment

<br/>

> A **production-grade** conversational AI agent that understands user intent, answers product questions via RAG, qualifies leads through natural conversation, and captures them to a real database — end to end.

<br/>

**[🌐 Live Demo](https://aesthetic-kitsune-f74820.netlify.app/)** · **[📹 Demo Video](https://youtu.be/64B2cnOab0Y)** · **[📋 Assignment](#-assignment-requirements--all-delivered)**

</div>

---

## ✅ Assignment Requirements — All Delivered

| # | Requirement | Status |
|---|---|---|
| 1 | Intent classification — greeting / inquiry / high-intent | ✅ Done |
| 2 | RAG-powered knowledge retrieval (FAISS + JSON KB) | ✅ Done |
| 3 | Lead qualification — name, email, platform | ✅ Done |
| 4 | mock_lead_capture() tool — fires only after all 3 fields | ✅ Done |
| 5 | LangGraph state management across 5–6 turns | ✅ Done |
| 6 | Python 3.9+ · LangChain · LangGraph | ✅ Done |
| 7 | requirements.txt | ✅ Done |
| 8 | README with architecture + WhatsApp deployment | ✅ Done |
| 9 | Demo video (2–3 minutes) | ✅ Done |

---

## ⭐ Beyond the Assignment — Extra Features Built

These were **not required** but built to demonstrate real-world production thinking:

| Extra Feature | Details |
|---|---|
| 🖥️ **Full Chat UI** | Custom dark-mode HTML/CSS/JS interface with live intent badge, lead progress tracker, and lead capture card |
| 🗄️ **Supabase Integration** | Every conversation turn and captured lead persisted to real PostgreSQL in real time |
| 🌐 **Live Public Deployment** | Fully deployed on Netlify — anyone can access and test without running locally |
| 📊 **Lead Dashboard** | All captured leads visible in Supabase Table Editor with session ID, timestamp, platform |
| 🧠 **Two-stage RAG** | Retrieval + formatting prompt — structured, accurate, hallucination-free responses |
| 🔄 **Multi-Provider LLM** | Switchable between Groq, OpenAI, Anthropic, Google via single config variable |
| 🧵 **Session Isolation** | Each browser session gets its own LangGraph thread ID — true multi-user concurrency |
| 📝 **Conversation Logging** | Full human + AI turn logging to Supabase `conversations` table with intent tagging |
| 🔌 **Flask API Backend** | Production `/chat` endpoint connecting UI → LangGraph → Supabase |

---

## 🎬 Demo

**Live demo:** [https://aesthetic-kitsune-f74820.netlify.app/](https://aesthetic-kitsune-f74820.netlify.app/)

**Video walkthrough:** [https://youtu.be/64B2cnOab0Y](https://youtu.be/64B2cnOab0Y)

```
┌─────────────────────────────────────────────────────────────────┐
│                     FULL CONVERSATION FLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  You   → "Hi there!"                                            │
│  Agent → "Welcome to AutoStream! We help content creators       │
│           edit videos automatically with AI..."                 │
│                                          Intent: 👋 greeting    │
│                                                                 │
│  You   → "How much is the Pro plan?"                            │
│  Agent → "The Pro Plan is $79/month — unlimited videos,         │
│           4K export, AI captions, 24/7 support..."              │
│                                       Intent: 🔍 inquiry        │
│                                                                 │
│  You   → "I want to sign up for my YouTube channel"             │
│  Agent → "Awesome! Could I get your full name first?"           │
│                                       Intent: 🔥 high intent    │
│                                                                 │
│  You   → "Raunit Singh"                                         │
│  Agent → "Nice to meet you! What's your email address?"         │
│                                                                 │
│  You   → "raunit@email.com"                                     │
│  Agent → "Which creator platform do you mainly use?"            │
│                                                                 │
│  You   → "YouTube"                                              │
│                                                                 │
│  ✅ Lead captured — mock_lead_capture() fired                   │
│  📦 Lead saved to Supabase database                             │
│  Agent → "You're all set! We'll reach out shortly. 🚀"          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

### System Flow

```
User Message (Browser UI)
         │
         ▼
┌─────────────────────┐
│   Flask API Server  │  POST /chat
│     server.py       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                  LangGraph Agent                    │
│                                                     │
│   START                                             │
│     │                                               │
│     ▼                                               │
│  intent_router ──────────────────────────────────── │─── log to Supabase
│     │                                               │
│     ├── greeting ──► greet_node ──► END             │
│     │                                               │
│     ├── product_inquiry ──► retrieve_node (RAG)     │
│     │                           │                   │
│     │                    FAISS vector search        │
│     │                    KB chunks → LLM → answer   │
│     │                           │                   │
│     │                          END                  │
│     │                                               │
│     └── high_intent ──► qualify_node                │
│                              │                      │
│                    name → email → platform          │
│                              │                      │
│                         all 3 filled?               │
│                              │                      │
│                    yes ──► capture_node             │
│                              │                      │
│                    mock_lead_capture()              │─── save to Supabase
│                              │                      │
│                             END                     │
└─────────────────────────────────────────────────────┘
         │
         ▼
  JSON Response → UI → Sidebar update
```

### Key Design Decisions

| Module | Role |
|---|---|
| `agent/graph.py` | LangGraph state machine — nodes, edges, conditional routing |
| `agent/intent.py` | LLM-powered intent classifier with output sanitization |
| `agent/nodes.py` | greet, retrieve, qualify, capture nodes |
| `agent/state.py` | AgentState TypedDict — single source of truth |
| `agent/memory.py` | MemorySaver checkpointer + Supabase conversation logger |
| `rag/loader.py` | Loads KB JSON into LangChain Documents (chunked by unit) |
| `rag/vectorstore.py` | Builds and persists FAISS index (smart: reuses existing) |
| `rag/retriever.py` | Top-K semantic similarity retriever |
| `rag/chain.py` | Full RAG chain — retriever → prompt → LLM → answer |
| `tools/lead_capture.py` | mock_lead_capture() + Supabase persistence |
| `server.py` | Flask API — /chat, /health, /ui endpoints |
| `ui/index.html` | Full chat UI with intent sidebar and lead card |

---

## 🧠 Architecture Explanation

### Why LangGraph?

LangGraph was chosen over a simple LangChain chain because this agent needs to make **routing decisions based on conversation state** — not just process text linearly. A greeting should never trigger lead capture. A high-intent signal mid-conversation must immediately switch to qualification mode. A user's name typed after "what's your name?" must not be misclassified as a product inquiry by the intent detector.

LangGraph's node-edge model makes all these conditional flows **explicit, testable, and structurally safe**. Each node does exactly one job. Routing is handled by conditional edges — not buried in prompt logic.

### How State Is Managed

Every turn passes through a shared `AgentState` TypedDict containing:
- `messages` — full conversation history via `add_messages` (merges, never overwrites)
- `intent` — latest classified intent
- `collected_name`, `collected_email`, `collected_platform` — lead fields filled incrementally
- `lead_captured` — boolean flag preventing double capture

The `intent_router` node reads state on every turn. Critically, **once qualification starts, the LLM classifier is bypassed entirely** — the router hardcodes `high_intent` so that names, emails, and platform answers are never misrouted. This was the most important design decision in the whole system.

LangGraph's `MemorySaver` checkpointer snapshots full state after every node. Each session uses a unique `thread_id`, enabling true multi-user isolation with no shared state.

### RAG Pipeline

The knowledge base (`autostream_kb.json`) is chunked by **semantic unit** — one chunk per plan, policy, FAQ, or feature. This gives the retriever precise, focused results rather than one giant blob. Chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2` (free, local, no API key) and stored in FAISS. On each product question, top-4 chunks are retrieved and injected into the LLM prompt with explicit instructions to answer only from context — making hallucination structurally impossible.

---

## 📱 WhatsApp Deployment via Webhooks

### Architecture

```
WhatsApp User
      │  sends message
      ▼
Meta WhatsApp Business API
      │  HTTP POST to your webhook URL
      ▼
FastAPI / Flask Server (/webhook endpoint)
      │  extract sender number + message text
      ▼
AutoStream LangGraph Agent
      │  thread_id = sender phone number
      │  full persistent memory per user
      ▼
Meta Graph API  ──  POST reply back
      │
      ▼
WhatsApp User receives agent response
```

### Step-by-Step Integration

**Step 1 — Create a Meta App**
- Go to [developers.facebook.com](https://developers.facebook.com)
- Create App → Add WhatsApp product
- Get a test phone number, `PHONE_NUMBER_ID`, and `ACCESS_TOKEN`

**Step 2 — Add webhook routes to server.py**

```python
import hmac, hashlib
from flask import request, jsonify
from langchain_core.messages import HumanMessage
from agent.graph import graph

VERIFY_TOKEN  = "your_secret_verify_token"
ACCESS_TOKEN  = "your_meta_access_token"
PHONE_NUM_ID  = "your_phone_number_id"

@app.get("/webhook/whatsapp")
def whatsapp_verify():
    """Meta calls this once to verify your webhook URL."""
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.post("/webhook/whatsapp")
def whatsapp_receive():
    """Receives every incoming WhatsApp message."""
    body    = request.get_json()
    entry   = body["entry"][0]["changes"][0]["value"]
    msg     = entry["messages"][0]
    sender  = msg["from"]           # unique per user — use as thread_id
    text    = msg["text"]["body"]

    # Run LangGraph agent — sender number = persistent memory per user
    config  = {"configurable": {"thread_id": sender}}
    result  = graph.invoke(
        {"messages": [HumanMessage(content=text)]},
        config=config
    )
    reply   = result["messages"][-1].content

    # Send reply via Meta Graph API
    import requests as req
    req.post(
        f"https://graph.facebook.com/v18.0/{PHONE_NUM_ID}/messages",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={
            "messaging_product": "whatsapp",
            "to": sender,
            "text": {"body": reply}
        }
    )
    return jsonify({"status": "ok"})
```

**Step 3 — Expose locally for testing**
```bash
pip install ngrok
ngrok http 8080
# Copy the HTTPS URL → paste into Meta webhook dashboard
```

**Step 4 — Register webhook in Meta dashboard**
- Webhook URL: `https://your-ngrok-url.ngrok.io/webhook/whatsapp`
- Verify token: same string as `VERIFY_TOKEN` above
- Subscribe to: `messages`

**Step 5 — Deploy to production**
```bash
# Railway, Render, or any cloud with public HTTPS
# Set environment variables:
#   GROQ_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_KEY
#   VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUM_ID
```

> The `thread_id = sender` pattern gives every WhatsApp user their own isolated conversation state with full memory — the exact same LangGraph graph and RAG pipeline work without any changes.

---

## 📁 Project Structure

```
social-to-lead-agentic/
│
├── config.py                    ← Central config, auto-detects LLM provider
├── main.py                      ← CLI entry point
├── server.py                    ← Flask API server (/chat, /health, /ui)
├── requirements.txt
├── .env.example
├── .gitignore
├── netlify.toml                 ← Netlify publish config
│
├── data/
│   ├── autostream_kb.json       ← Knowledge base: pricing, plans, policies
│   └── faiss_index/             ← Auto-generated vector store
│
├── rag/
│   ├── loader.py                ← KB → LangChain Documents
│   ├── vectorstore.py           ← FAISS build & smart load
│   ├── retriever.py             ← Top-K similarity retrieval
│   └── chain.py                 ← Full RAG chain
│
├── agent/
│   ├── state.py                 ← AgentState TypedDict
│   ├── intent.py                ← LLM intent classifier
│   ├── nodes.py                 ← greet / retrieve / qualify / capture
│   ├── graph.py                 ← Compiled LangGraph
│   └── memory.py                ← MemorySaver + Supabase logger
│
├── tools/
│   └── lead_capture.py          ← mock_lead_capture() + Supabase save
│
└── ui/
    └── index.html               ← Full chat UI
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Free Groq API key → [console.groq.com](https://console.groq.com)
- Supabase project (optional) → [supabase.com](https://supabase.com)

### 1. Clone
```bash
git clone https://github.com/raunitsingh/social-to-lead-agentic.git
cd social-to-lead-agentic
```

### 2. Virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
nano .env
```
```env
GROQ_API_KEY=gsk_your_key_here
LLM_MODEL=llama-3.3-70b-versatile

# Optional — agent works without these, Supabase adds persistence
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
```

### 5. Set Python path
```bash
export PYTHONPATH="$(pwd)"
```

### 6. Run
```bash
python server.py
```

### 7. Open UI
```
http://localhost:8080/ui/index.html
```

> First run downloads the embedding model (~90MB). Subsequent runs load the saved FAISS index instantly.

---

## 🗄️ Database Schema (Supabase)

```sql
-- Captured leads
CREATE TABLE leads (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  text,
    name        text NOT NULL,
    email       text NOT NULL,
    platform    text NOT NULL,
    captured_at timestamptz DEFAULT now(),
    source      text DEFAULT 'autostream-agent'
);

-- Full conversation log
CREATE TABLE conversations (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  text,
    role        text,       -- 'human' | 'ai'
    content     text,
    intent      text,
    created_at  timestamptz DEFAULT now()
);
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph 0.4+ |
| LLM | Groq — LLaMA 3.3 70B (free tier) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 (local, free) |
| Vector Store | FAISS (local, no server needed) |
| Backend | Flask |
| Database | Supabase (PostgreSQL) |
| Frontend | HTML / CSS / JavaScript |
| Deployment | Netlify (UI) |

---

## 📊 Evaluation Criteria

| Criterion | Implementation |
|---|---|
| Agent reasoning & intent detection | LLM classifier with sanitized output — 8/8 test cases pass |
| Correct use of RAG | FAISS + HuggingFace + LangChain — KB-grounded, no hallucinations |
| Clean state management | AgentState TypedDict + MemorySaver — full isolation per thread |
| Proper tool calling logic | Fires only after name + email + platform all confirmed in state |
| Code clarity & structure | One responsibility per file, fully typed and documented |
| Real-world deployability | Live on Netlify + WhatsApp webhook architecture documented |

---

<div align="center">

Built by **Raunit singh** for the **Machine Learning Intern** role at **ServiceHive / Inflx**

**[🌐 Live Demo](https://aesthetic-kitsune-f74820.netlify.app/)** · **[📹 Demo Video](https://youtu.be/64B2cnOab0Y)**

</div>