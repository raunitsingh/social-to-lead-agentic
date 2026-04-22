from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import LLM_PROVIDER, LLM_MODEL, logger


# ── Load LLM ─────────────────────────────────────────────────────────────────
def _load_llm():
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq
        from config import GROQ_API_KEY
        return ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)

    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        from config import ANTHROPIC_API_KEY
        return ChatAnthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY, temperature=0)

    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        from config import OPENAI_API_KEY
        return ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0)

    if LLM_PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        from config import GOOGLE_API_KEY
        return ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0)

    raise ValueError(f"Unsupported provider: {LLM_PROVIDER}")


# ── Intent classification prompt ──────────────────────────────────────────────
_INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an intent classifier for AutoStream, a video editing SaaS.

Classify the user message into EXACTLY one of these three labels:

  greeting        - casual greetings, small talk, hello, hi, how are you
  product_inquiry - questions about pricing, features, plans, refunds, support
  high_intent     - user wants to sign up, buy, start a trial, get the pro plan,
                    or shows clear purchase intent

Reply with ONLY the label — no punctuation, no explanation, nothing else.
Examples:
  "Hi there!"                              → greeting
  "How much does the Pro plan cost?"       → product_inquiry
  "I want to try AutoStream for YouTube"   → high_intent
  "Does it support 4K?"                    → product_inquiry
  "Sign me up for the Pro plan"            → high_intent
  "What's your refund policy?"             → product_inquiry
"""),
    ("human", "{message}"),
])


# ── Build classifier chain ────────────────────────────────────────────────────
def build_intent_classifier():
    """Returns a callable: classify(message: str) -> str"""
    llm    = _load_llm()
    chain  = _INTENT_PROMPT | llm | StrOutputParser()

    def classify(message: str) -> str:
        raw    = chain.invoke({"message": message}).strip().lower()
        # Sanitize — only accept known labels
        if raw in ("greeting", "product_inquiry", "high_intent"):
            intent = raw
        elif "greeting" in raw:
            intent = "greeting"
        elif "high" in raw or "intent" in raw:
            intent = "high_intent"
        elif "inquiry" in raw or "product" in raw:
            intent = "product_inquiry"
        else:
            intent = "product_inquiry"   # safe default

        logger.info(f"Intent classified: '{message[:40]}...' → {intent}")
        return intent

    return classify


if __name__ == "__main__":
    classify = build_intent_classifier()

    tests = [
        ("Hi! How are you?",                          "greeting"),
        ("What is the price of the Pro plan?",        "product_inquiry"),
        ("I want to sign up for YouTube editing",     "high_intent"),
        ("Does Basic plan support 4K resolution?",    "product_inquiry"),
        ("I'd like to try the Pro plan",              "high_intent"),
        ("What's your refund policy?",                "product_inquiry"),
        ("Hey",                                       "greeting"),
        ("Sign me up, I create content on Instagram", "high_intent"),
    ]

    print("\n── Intent Classification Test ───────────────────────────\n")
    passed = 0
    for msg, expected in tests:
        result = classify(msg)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        print(f"  {status}  [{result:16s}]  {msg}")

    print(f"\n  {passed}/{len(tests)} passed\n")