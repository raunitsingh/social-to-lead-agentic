# 🎬 AutoStream AI Sales Agent
### Social-to-Lead Agentic Workflow — ServiceHive × Inflx Assignment

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/LangGraph-Agentic-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/FAISS-RAG_Pipeline-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Supabase-Database-teal?style=for-the-badge"/>
  🌐 **Live Demo:** https://aesthetic-kitsune-f74820.netlify.app
</p>

> A production-grade conversational AI agent for **AutoStream** — an AI-powered video editing SaaS. Built with LangGraph, FAISS-powered RAG, real-time lead capture, Supabase persistence, and a fully functional chat UI.

---

## 🚀 Live Demo

**🌐 Try it now:** [`aesthetic-kitsune-f74820.netlify.app/`](https://nemeses-deflator-aspirin.ngrok-free.app/ui/index.html)

> Click **"Visit Site"** on the ngrok warning page to access the demo.

---

## ✅ Assignment Requirements — All Delivered

| Requirement | Status |
|---|---|
| Intent classification (greeting / inquiry / high-intent) | ✅ Done |
| RAG-powered knowledge retrieval (FAISS + JSON KB) | ✅ Done |
| Lead qualification (name, email, platform) | ✅ Done |
| Mock lead capture tool execution | ✅ Done |
| LangGraph state management across 5–6 turns | ✅ Done |
| Python 3.9+, LangChain / LangGraph | ✅ Done |
| requirements.txt | ✅ Done |
| README with architecture + WhatsApp deployment | ✅ Done |
| Demo video | ✅ Done |

---

## ⭐ Beyond the Assignment — Extra Features Built

These were **not required** but were built to demonstrate real-world production thinking:

| Extra Feature | Details |
|---|---|
| 🖥️ **Full Chat UI** | Custom HTML/CSS/JS chat interface with live sidebar showing intent, collected lead fields, and lead card on capture |
| 🗄️ **Supabase Integration** | Every conversation turn and captured lead is persisted to a real Postgres database in real time |
| 🌐 **Live Public Deployment** | Exposed via ngrok — anyone can access and use the agent without running it locally |
| 📊 **Lead Dashboard** | Captured leads visible in Supabase Table Editor with session ID, timestamp, platform |
| 🧠 **Rich RAG Responses** | Two-stage LLM pipeline: RAG retrieval + formatting prompt for structured, emoji-rich responses |
| 🔄 **Multi-Provider LLM Support** | Switchable between Groq, OpenAI, Anthropic, and Google via a single config variable |
| 🧵 **Session Management** | Each browser session gets its own LangGraph thread ID, enabling true multi-user concurrency |
| 📝 **Conversation Logging** | Full human + AI turn logging to Supabase `conversations` table with intent tagging |

---

## 🏗️ Architecture

```
User Message (UI)
      │
      ▼
┌─────────────┐
│  Flask API  │  server.py — /chat endpoint
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  LangGraph Graph │
│                  │
│  START           │
│    │             │
│    ▼             │
│  intent_router ──┼─── Logs human message to Supabase
│    │             │
│    ▼             │
│  route_by_intent │
│  ┌──┬──┬──┐     │
│  ▼  ▼  ▼  │     │
│ greet retrieve qualify
│  │    │    │     │
│  │    │    ▼     │
│  │    │  capture_node ── tools/lead_capture.py ── Supabase leads table
│  │    │    │     │
│  └────┴────┘     │
│       │          │
│      END         │
└──────────────────┘
       │
       ▼
  JSON Response → UI
```

### Key Components

| Module | Role |
|---|---|
| `agent/graph.py` | LangGraph state machine — nodes, edges, conditional routing |
| `agent/intent.py` | LLM-powered intent classifier (greeting / product_inquiry / high_intent) |
| `agent/nodes.py` | greet, retrieve, qualify, capture nodes |
| `agent/state.py` | TypedDict state schema shared across all nodes |
| `agent/memory.py` | MemorySaver checkpointer + Supabase conversation logger |
| `rag/loader.py` | Loads `autostream_kb.json` into LangChain Documents |
| `rag/vectorstore.py` | Builds and persists FAISS index |
| `rag/retriever.py` | Top-K semantic similarity retriever |
| `rag/chain.py` | Full RAG chain — retriever → prompt → LLM → parser |
| `tools/lead_capture.py` | Lead capture tool — saves to Supabase + prints confirmation |
| `ui/index.html` | Full chat UI with intent sidebar and lead card |
| `server.py` | Flask server exposing `/chat`, `/health`, `/ui/` |
| `data/autostream_kb.json` | Knowledge base — pricing, features, policies |

---

## 🧠 Architecture Explanation (~200 words)

**Why LangGraph?**
LangGraph was chosen over a simple chain because the agent needs to behave differently depending on *state* — not just the last message. A greeting should never trigger lead capture; a high-intent signal mid-conversation should immediately switch to qualification, regardless of what the user said. LangGraph's node-edge model makes these conditional flows explicit, testable, and easy to extend. It also provides a built-in checkpointer (MemorySaver) that retains full conversation state across turns per thread ID — enabling true multi-turn memory without manual message history management.

**How State Is Managed:**
Every conversation turn passes through a shared `AgentState` TypedDict containing: message history, detected intent, and incrementally collected lead fields (`collected_name`, `collected_email`, `collected_platform`). The `intent_router` node reads this state to decide whether to continue qualification or re-route. The `qualify_node` uses sentinel values (`None` vs `""`) to track exactly which fields have been collected, ensuring the lead capture tool is never called prematurely. Each browser session maps to a unique LangGraph `thread_id`, enabling full isolation between concurrent users.

---

## 📱 WhatsApp Deployment via Webhooks

To deploy this agent on WhatsApp using the **WhatsApp Business API (Meta)**:

1. **Register a WhatsApp Business App** on Meta for Developers and obtain a `PHONE_NUMBER_ID` and `ACCESS_TOKEN`.

2. **Set up a Webhook endpoint** — add a new route to `server.py`:
   ```python
   @app.post("/webhook/whatsapp")
   def whatsapp_webhook():
       data = request.get_json()
       message = data["entry"][0]["changes"][0]["value"]["messages"][0]
       user_phone = message["from"]
       user_text  = message["text"]["body"]
       # Use phone number as session_id for state isolation
       reply = invoke_graph(user_text, session_id=user_phone)
       send_whatsapp_reply(user_phone, reply)
       return jsonify({"status": "ok"})
   ```

3. **Verify the webhook** — Meta sends a GET request with a `hub.verify_token` that your server must echo back.

4. **Send replies** using the WhatsApp Cloud API:
   ```python
   import requests
   def send_whatsapp_reply(to, text):
       requests.post(
           f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
           headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
           json={"messaging_product": "whatsapp", "to": to, "text": {"body": text}}
       )
   ```

5. **Deploy** the Flask server to a public HTTPS URL (e.g. Railway, Render, or EC2) — Meta requires HTTPS for webhooks. The same LangGraph graph and RAG pipeline work without any changes.

---

## 🛠️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/raunitsingh/social-to-lead-agentic.git
cd social-to-lead-agentic
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```env
# LLM Provider — choose one: groq | openai | anthropic | google
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

# API Keys (only the one matching your provider is required)
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# Supabase (optional — agent works without it, Supabase just adds persistence)
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

### 5. Run the server
```bash
python server.py
```

### 6. Open the UI
```
http://localhost:8080/ui/index.html
```

---

## 💬 Example Conversation Flow

```
User:  Hi there!
Agent: Hey there! 👋 Welcome to AutoStream — the AI-powered video editing
       platform built for content creators. I can help you explore our
       pricing, features, or get you signed up. What would you like to know?

User:  What's the Pro plan price?
Agent: The **Pro Plan** is **$79/month** and includes:
       • Unlimited videos • 4K resolution export • AI captions
       • Priority 24/7 support • Auto-publish to YouTube, Instagram & TikTok
       • Analytics dashboard
       Want to sign up? 🚀

User:  I want to try the Pro plan for my YouTube channel
Agent: Awesome! 🎉 I'd love to get you started. Could I get your full name first?

User:  Raunit Singh
Agent: Nice to meet you, Raunit! 😊 What's your email address?

User:  raunit@email.com
Agent: Perfect! Last one — which creator platform do you mainly use?

User:  YouTube
Agent: You're all set, Raunit! 🚀 Our team will reach out to raunit@email.com
       within 24 hours to activate your AutoStream account. Welcome aboard!
```

---

## 📁 Project Structure

```
social-to-lead-agentic/
├── agent/
│   ├── graph.py          # LangGraph state machine
│   ├── intent.py         # Intent classifier
│   ├── memory.py         # Checkpointer + Supabase logger
│   ├── nodes.py          # greet, retrieve, qualify, capture nodes
│   └── state.py          # AgentState TypedDict
├── data/
│   └── autostream_kb.json  # Knowledge base
├── rag/
│   ├── chain.py          # RAG chain
│   ├── loader.py         # KB loader
│   ├── retriever.py      # FAISS retriever
│   └── vectorstore.py    # FAISS index builder
├── tools/
│   └── lead_capture.py   # Lead capture tool
├── ui/
│   └── index.html        # Chat UI
├── config.py             # Centralised config + logging
├── server.py             # Flask API server
├── supabase.sql          # DB schema
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Schema (Supabase)

**`leads` table** — one row per captured lead
```sql
id, session_id, name, email, platform, captured_at, source
```

**`conversations` table** — one row per message turn
```sql
id, session_id, role, content, intent, created_at
```

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph 0.2+ |
| LLM | Groq — LLaMA 3.3 70B |
| RAG | FAISS + LangChain |
| Backend | Flask |
| Database | Supabase (PostgreSQL) |
| Frontend | HTML / CSS / JavaScript |
| Deployment | ngrok |

---

## 👤 Author

**Raunit Singh**
Assignment submission for **Machine Learning Intern** role at **ServiceHive**