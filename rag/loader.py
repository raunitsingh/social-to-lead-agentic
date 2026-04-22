import json
from pathlib import Path
from typing import List

from langchain.schema import Document


def load_kb(kb_path: Path) -> List[Document]:
    """
    Load the knowledge base JSON and return a list of LangChain Documents.
    Each Document = one chunk with metadata for traceability.
    """
    with open(kb_path, "r") as f:
        kb = json.load(f)

    docs: List[Document] = []

    # ── Company overview ──────────────────────────────────────────────────────
    company = kb.get("company", {})
    docs.append(Document(
        page_content=(
            f"Company: {company.get('name')}\n"
            f"About: {company.get('description')}\n"
            f"Tagline: {company.get('tagline')}"
        ),
        metadata={"source": "company_overview"}
    ))

    # ── Pricing plans ─────────────────────────────────────────────────────────
    for plan in kb.get("plans", []):
        features = "\n  - ".join(plan.get("features", []))
        limitations = plan.get("limitations", [])
        lim_text = ("\nLimitations:\n  - " + "\n  - ".join(limitations)) if limitations else ""

        docs.append(Document(
            page_content=(
                f"Plan: {plan['name']}\n"
                f"Price: ${plan['price_monthly']}/month\n"
                f"Features:\n  - {features}"
                f"{lim_text}\n"
                f"Best for: {plan.get('best_for', '')}"
            ),
            metadata={"source": "pricing", "plan": plan["name"]}
        ))

    # ── Policies ─────────────────────────────────────────────────────────────
    for policy in kb.get("policies", []):
        docs.append(Document(
            page_content=(
                f"Policy: {policy['policy']}\n"
                f"Details: {policy['details']}"
            ),
            metadata={"source": "policy", "policy": policy["policy"]}
        ))

    # ── Pricing FAQ ───────────────────────────────────────────────────────────
    for faq in kb.get("pricing_faq", []):
        docs.append(Document(
            page_content=(
                f"Q: {faq['question']}\n"
                f"A: {faq['answer']}"
            ),
            metadata={"source": "faq"}
        ))

    # ── Feature details ───────────────────────────────────────────────────────
    for feat in kb.get("features_detail", []):
        available = ", ".join(feat.get("available_on", []))
        docs.append(Document(
            page_content=(
                f"Feature: {feat['feature']}\n"
                f"Available on: {available}\n"
                f"Description: {feat['description']}"
            ),
            metadata={"source": "feature", "feature": feat["feature"]}
        ))

    return docs


if __name__ == "__main__":
    from config import KB_PATH
    docs = load_kb(KB_PATH)
    print(f"Loaded {len(docs)} chunks from knowledge base:\n")
    for i, doc in enumerate(docs):
        print(f"[{i+1}] source={doc.metadata['source']}")
        print(f"     {doc.page_content[:80]}...")
        print()