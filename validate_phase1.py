import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent

PASS = "  ✓"
FAIL = "  ✗"
WARN = "  ⚠"


def check(label: str, condition: bool, hint: str = "") -> bool:
    if condition:
        print(f"{PASS}  {label}")
    else:
        print(f"{FAIL}  {label}")
        if hint:
            print(f"      → {hint}")
    return condition


def section(title: str) -> None:
    print(f"\n── {title} {'─' * (50 - len(title))}")


all_ok = True

# ─── 1. Directory structure ───────────────────────────────────────────────────
section("Directory Structure")
required_dirs = ["agent", "rag", "tools", "data", "tests"]
for d in required_dirs:
    ok = (ROOT / d).is_dir()
    all_ok &= check(f"/{d}/ directory exists", ok, f"Run: mkdir {d}")

# ─── 2. Required files ────────────────────────────────────────────────────────
section("Required Files")
required_files = {
    "config.py":              "Central config — should be in project root",
    "requirements.txt":       "Dependency list",
    ".gitignore":             "Git ignore file",
    ".env.example":           "Env template",
    "data/autostream_kb.json":"Knowledge base",
    "agent/__init__.py":      "Agent package init",
    "rag/__init__.py":        "RAG package init",
    "tools/__init__.py":      "Tools package init",
    "tests/__init__.py":      "Tests package init",
}
for path, hint in required_files.items():
    ok = (ROOT / path).exists()
    all_ok &= check(path, ok, f"Missing: {hint}")

# ─── 3. .env file ────────────────────────────────────────────────────────────
section(".env API Key Check")
env_path = ROOT / ".env"
if not env_path.exists():
    print(f"{WARN}  .env file not found — copy .env.example → .env and fill in your key")
    all_ok = False
else:
    content = env_path.read_text()
    has_key = any(
        line.startswith(k) and not line.strip().endswith("_here")
        for k in ("ANTHROPIC_API_KEY=", "OPENAI_API_KEY=", "GOOGLE_API_KEY=")
        for line in content.splitlines()
    )
    all_ok &= check(
        "At least one API key set in .env",
        has_key,
        "Edit .env and add your ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY"
    )

# ─── 4. Knowledge base validation ─────────────────────────────────────────────
section("Knowledge Base Validation")
kb_path = ROOT / "data" / "autostream_kb.json"
if kb_path.exists():
    try:
        with open(kb_path) as f:
            kb = json.load(f)

        all_ok &= check("KB is valid JSON", True)
        all_ok &= check("KB has 'company' key",  "company" in kb,  "Add company info to KB")
        all_ok &= check("KB has 'plans' key",    "plans" in kb,    "Add pricing plans to KB")
        all_ok &= check("KB has 'policies' key", "policies" in kb, "Add policies to KB")

        plans = kb.get("plans", [])
        all_ok &= check("At least 2 plans defined", len(plans) >= 2, "Add Basic and Pro plans")

        plan_names = [p.get("name", "") for p in plans]
        all_ok &= check("Basic Plan present", any("Basic" in n for n in plan_names))
        all_ok &= check("Pro Plan present",   any("Pro"   in n for n in plan_names))

        # Check pricing
        for plan in plans:
            name  = plan.get("name", "Unknown")
            price = plan.get("price_monthly")
            feats = plan.get("features", [])
            all_ok &= check(f"{name}: has price_monthly", price is not None)
            all_ok &= check(f"{name}: has features list", len(feats) > 0)

        policies = kb.get("policies", [])
        policy_names = [p.get("policy", "") for p in policies]
        all_ok &= check(
            "Refund policy defined",
            any("Refund" in n for n in policy_names),
            "Add refund policy to KB"
        )
        all_ok &= check(
            "Support policy defined",
            any("Support" in n for n in policy_names),
            "Add support policy to KB"
        )

    except json.JSONDecodeError as e:
        all_ok = False
        check("KB is valid JSON", False, f"JSON error: {e}")
else:
    all_ok = False
    print(f"{FAIL}  KB file not found — skipping KB validation")

# ─── 5. config.py import test ─────────────────────────────────────────────────
section("Config Module Import")
try:
    # Only import if .env exists to avoid misleading errors
    if (ROOT / ".env").exists():
        sys.path.insert(0, str(ROOT))
        import config  # noqa: F401
        check("config.py imports without error", True)
        print(f"      Provider detected: {config.LLM_PROVIDER}")
        print(f"      Model            : {config.LLM_MODEL}")
    else:
        print(f"{WARN}  Skipping config import — .env not found yet")
except Exception as e:
    all_ok = False
    check("config.py imports without error", False, str(e))

# ─── Summary ──────────────────────────────────────────────────────────────────
print("\n" + "─" * 55)
if all_ok:
    print("  🎉  Phase 1 complete! All checks passed.")
    print("      Ready to build Phase 2 — RAG Pipeline.")
else:
    print("  ⚠   Some checks failed. Fix the issues above, then re-run.")
print("─" * 55 + "\n")

sys.exit(0 if all_ok else 1)
