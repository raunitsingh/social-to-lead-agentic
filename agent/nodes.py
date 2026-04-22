from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import LLM_PROVIDER, LLM_MODEL, logger
from agent.state import AgentState
from agent.memory import log_message
from rag.chain import build_rag_chain


def _load_llm(temperature=0.4):
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq
        from config import GROQ_API_KEY
        return ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=temperature)
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        from config import ANTHROPIC_API_KEY
        return ChatAnthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY, temperature=temperature)
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        from config import OPENAI_API_KEY
        return ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=temperature)
    raise ValueError(f"Unsupported provider: {LLM_PROVIDER}")


def _last_human_message(state):
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            return msg.content
    return ""


def _thread_id(config):
    return config.get("configurable", {}).get("thread_id")


# ── Greet node ────────────────────────────────────────────────────────────────

_GREET_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly, enthusiastic sales assistant for AutoStream — an AI-powered video editing SaaS built for content creators.

When greeting a user:
- Welcome them warmly with an emoji
- Introduce AutoStream in ONE punchy sentence
- Tell them you can help with: pricing, features, or signing up
- Keep it 2-3 sentences, conversational tone

Example:
"Hey there! 👋 Welcome to **AutoStream** — the AI-powered video editing platform built for content creators.
I can help you explore our plans, answer questions, or get you signed up. What would you like to know?"
"""),
    ("human", "{message}"),
])

def greet_node(state, config):
    logger.info("Node: greet_node")
    llm   = _load_llm()
    chain = _GREET_PROMPT | llm | StrOutputParser()
    reply = chain.invoke({"message": _last_human_message(state)})
    log_message(_thread_id(config), "ai", reply, "greeting")
    return {"messages": [AIMessage(content=reply)], "intent": "greeting"}


# ── Retrieve node (RAG) ───────────────────────────────────────────────────────

_rag_chain = None

def _get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        from config import KB_PATH, VECTORSTORE_PATH, RAG_TOP_K
        from rag.loader import load_kb
        from rag.vectorstore import get_vectorstore
        from rag.retriever import get_retriever
        docs      = load_kb(KB_PATH)
        vs        = get_vectorstore(docs, VECTORSTORE_PATH)
        retriever = get_retriever(vs, top_k=RAG_TOP_K)
        _rag_chain = build_rag_chain(retriever)
    return _rag_chain


_RAG_ENHANCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert sales assistant for AutoStream, an AI-powered video editing SaaS.

Retrieved context from knowledge base:
{context}

STRICT RESPONSE RULES:
1. Use **bold** for plan names, prices, and key features
2. Use bullet points (•) when listing features — list ALL of them, never summarise
3. Always show the EXACT price ($29/mo or $79/mo)
4. For Pro Plan: always list → Unlimited videos • 4K resolution export • AI captions (95%+ accuracy, 20+ languages) • Priority 24/7 support • Auto-publish to YouTube, Instagram & TikTok • Analytics dashboard
5. For Basic Plan: always list → 10 videos/month • 720p resolution • Auto-cut & trim • Email support (48hr response)
6. For refund questions: mention the exact 7-day window
7. End every answer with a soft CTA: "Want to sign up?" or "Which plan suits you?" or "Any other questions?"
8. Be warm and conversational, not robotic
9. Use 1-2 relevant emojis per response

KNOWLEDGE (use these exact figures):
- Basic: $29/month | Pro: $79/month
- No refunds after 7 days | 24/7 support Pro only | Cancel anytime
"""),
    ("human", "Question: {question}"),
])

def retrieve_node(state, config):
    logger.info("Node: retrieve_node")
    question = _last_human_message(state)

    # Get RAG context from vectorstore
    try:
        raw_context = _get_rag_chain().invoke({"question": question})
    except Exception:
        raw_context = "No additional context retrieved."

    # Enhance with rich formatting prompt
    llm   = _load_llm(temperature=0.3)
    chain = _RAG_ENHANCE_PROMPT | llm | StrOutputParser()
    reply = chain.invoke({"question": question, "context": raw_context})

    log_message(_thread_id(config), "ai", reply, "product_inquiry")
    return {"messages": [AIMessage(content=reply)], "intent": "product_inquiry"}


# ── Qualify node ──────────────────────────────────────────────────────────────

def qualify_node(state, config=None):
    logger.info("Node: qualify_node")
    message  = _last_human_message(state)
    name     = state.get("collected_name")
    email    = state.get("collected_email")
    platform = state.get("collected_platform")

    if name is None and email is None and platform is None:
        reply = "Awesome! 🎉 I'd love to get you started with AutoStream.\n\nCould I get your **full name** first?"
        log_message(_thread_id(config), "ai", reply, "high_intent")
        return {"messages": [AIMessage(content=reply)], "collected_name": "", "intent": "high_intent"}

    if name == "":
        reply = f"Nice to meet you, **{message}**! 😊\n\nWhat's your **email address**?"
        log_message(_thread_id(config), "ai", reply, "high_intent")
        return {"messages": [AIMessage(content=reply)], "collected_name": message, "intent": "high_intent"}

    if email is None:
        reply = "Perfect! Last one — which **creator platform** do you mainly use?\n*(YouTube, Instagram, TikTok, etc.)*"
        log_message(_thread_id(config), "ai", reply, "high_intent")
        return {"messages": [AIMessage(content=reply)], "collected_email": message, "intent": "high_intent"}

    if platform is None:
        return {"messages": [], "collected_platform": message, "intent": "high_intent"}

    return {"messages": [], "intent": "high_intent"}


# ── Capture node ──────────────────────────────────────────────────────────────

def capture_node(state, config=None):
    logger.info("Node: capture_node")
    name     = state.get("collected_name")
    email    = state.get("collected_email")
    platform = state.get("collected_platform")

    if not all([name, email, platform]):
        return {"messages": [AIMessage(content="I still need a few more details.")]}

    from tools.lead_capture import capture_lead
    capture_lead(
        name       = name,
        email      = email,
        platform   = platform,
        session_id = _thread_id(config),
    )

    reply = (
        f"You're all set, **{name}**! 🚀\n\n"
        f"Our team will reach out to **{email}** within 24 hours "
        f"to activate your AutoStream account. Welcome aboard!"
    )
    log_message(_thread_id(config), "ai", reply, "high_intent")
    return {"messages": [AIMessage(content=reply)], "lead_captured": True}