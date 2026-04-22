from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # ── Conversation history ──────────────────────────────────────────────────
    # add_messages merges new messages into the list instead of overwriting
    messages: Annotated[List[BaseMessage], add_messages]

    # ── Intent detected in the latest turn ───────────────────────────────────
    # Values: "greeting" | "product_inquiry" | "high_intent" | "unknown"
    intent: Optional[str]

    # ── Lead collection fields (filled one by one in qualify_node) ────────────
    collected_name:     Optional[str]
    collected_email:    Optional[str]
    collected_platform: Optional[str]

    # ── Flag: has the lead capture tool been fired? ───────────────────────────
    lead_captured: bool