import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env from project root ───────────────────────────────────────────────
_ROOT = Path(__file__).parent
load_dotenv(_ROOT / ".env")


# ── Logging ───────────────────────────────────────────────────────────────────
_log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
_log_level = getattr(logging, _log_level_str, logging.INFO)

logging.basicConfig(
    level=_log_level,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("autostream")


# ── LLM Provider Detection ────────────────────────────────────────────────────
def _detect_provider() -> str:
    """Auto-detect which LLM provider to use based on available API keys."""
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GOOGLE_API_KEY"):
        return "google"
    raise EnvironmentError(
        "\n\n  No LLM API key found in .env\n"
        "  Add one of the following to your .env file:\n\n"
        "    GROQ_API_KEY=your_key_here          <- free, recommended\n"
        "    ANTHROPIC_API_KEY=your_key_here\n"
        "    OPENAI_API_KEY=your_key_here\n"
        "    GOOGLE_API_KEY=your_key_here\n"
    )


# ── API Keys ──────────────────────────────────────────────────────────────────
GROQ_API_KEY: str      = os.getenv("GROQ_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY: str    = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY: str    = os.getenv("GOOGLE_API_KEY", "")

# ── LLM Provider & Model ──────────────────────────────────────────────────────
LLM_PROVIDER: str = _detect_provider()

# Default models per provider if LLM_MODEL is not set in .env
_DEFAULT_MODELS = {
    "groq":      "llama-3.3-70b-versatile",
    "anthropic": "claude-3-haiku-20240307",
    "openai":    "gpt-4o-mini",
    "google":    "gemini-1.5-flash",
}

LLM_MODEL: str = os.getenv("LLM_MODEL") or _DEFAULT_MODELS[LLM_PROVIDER]

# ── Paths ─────────────────────────────────────────────────────────────────────
KB_PATH: Path          = _ROOT / os.getenv("KB_PATH", "data/autostream_kb.json")
VECTORSTORE_PATH: Path = _ROOT / os.getenv("VECTORSTORE_PATH", "data/faiss_index")

# ── RAG ───────────────────────────────────────────────────────────────────────
RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "4"))

# ── Guard: KB must exist ──────────────────────────────────────────────────────
if not KB_PATH.exists():
    raise FileNotFoundError(
        f"\n  Knowledge base not found at: {KB_PATH}\n"
        f"  Make sure data/autostream_kb.json exists.\n"
    )


# ── Convenience printer ───────────────────────────────────────────────────────
def print_config() -> None:
    """Print current config (masks API keys)."""
    active_key = GROQ_API_KEY or ANTHROPIC_API_KEY or OPENAI_API_KEY or GOOGLE_API_KEY

    def mask(val: str) -> str:
        return val[:8] + "..." + val[-4:] if len(val) > 14 else "***"

    print("\n-- AutoStream Agent Config -----------------------------")
    print(f"  Provider      : {LLM_PROVIDER}")
    print(f"  Model         : {LLM_MODEL}")
    print(f"  API Key       : {mask(active_key)}")
    print(f"  KB Path       : {KB_PATH}")
    print(f"  VectorStore   : {VECTORSTORE_PATH}")
    print(f"  RAG Top-K     : {RAG_TOP_K}")
    print(f"  Log Level     : {_log_level_str}")
    print("--------------------------------------------------------\n")


if __name__ == "__main__":
    print_config()