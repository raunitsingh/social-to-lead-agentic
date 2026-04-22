from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.intent import build_intent_classifier
from agent.nodes import greet_node, retrieve_node, qualify_node, capture_node
from agent.memory import checkpointer, log_message          # ← EDIT 1: added log_message
from config import logger

_classify = build_intent_classifier()


def intent_router(state, config):                           # ← EDIT 2: added config param
    from langchain_core.messages import HumanMessage

    # ── EDIT 3: log the incoming human message ────────────────────────────────
    thread_id = config["configurable"]["thread_id"]
    user_msg  = state["messages"][-1].content
    log_message(thread_id, "human", user_msg, state.get("intent"))
    # ─────────────────────────────────────────────────────────────────────────

    in_qualification = (
        state.get("collected_name")     is not None
        or state.get("collected_email")    is not None
        or state.get("collected_platform") is not None
    )
    if in_qualification:
        return {"intent": "high_intent"}
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            return {"intent": _classify(msg.content)}
    return {"intent": "product_inquiry"}


def route_by_intent(state):
    intent = state.get("intent", "product_inquiry")
    if (intent == "high_intent"
            or state.get("collected_name")     is not None
            or state.get("collected_email")    is not None
            or state.get("collected_platform") is not None):
        return "qualify"
    if intent == "greeting":
        return "greet"
    return "retrieve"


def should_capture(state):
    if all([state.get("collected_name"), state.get("collected_email"), state.get("collected_platform")]):
        return "capture"
    return END


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("intent_router", intent_router)
    builder.add_node("greet_node",    greet_node)
    builder.add_node("retrieve_node", retrieve_node)
    builder.add_node("qualify_node",  qualify_node)
    builder.add_node("capture_node",  capture_node)
    builder.add_edge(START, "intent_router")
    builder.add_conditional_edges("intent_router", route_by_intent,
            {"greet": "greet_node", "retrieve": "retrieve_node", "qualify": "qualify_node"})
    builder.add_conditional_edges("qualify_node", should_capture,
            {"capture": "capture_node", END: END})
    builder.add_edge("greet_node",    END)
    builder.add_edge("retrieve_node", END)
    builder.add_edge("capture_node",  END)
    graph = builder.compile(checkpointer=checkpointer)
    logger.info("LangGraph compiled successfully")
    return graph

graph = build_graph()