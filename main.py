import uuid
import sys
from langchain_core.messages import HumanMessage

from config import print_config, logger


def main() -> None:
    print("\n" + "═" * 55)
    print("  AutoStream Conversational AI Agent")
    print("  ServiceHive / Inflx — ML Internship Build")
    print("═" * 55)
    print_config()

    # ── Import graph (builds RAG + LangGraph on first run) ────────────────────
    print("  Loading agent... (first run downloads embedding model ~90MB)\n")
    from agent.graph import graph

    # ── Unique session ID — each run gets fresh memory ────────────────────────
    thread_id = str(uuid.uuid4())
    config    = {"configurable": {"thread_id": thread_id}}

    print("  Agent ready! Type 'exit' to quit.\n")
    print("─" * 55)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            print("Agent: Thanks for chatting! Have a great day. 👋")
            break

        # ── Run one turn through the graph ────────────────────────────────────
        result = graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        # ── Print the agent's last reply ──────────────────────────────────────
        reply = result["messages"][-1].content
        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    try:
        main()
    except EnvironmentError as e:
        print(f"\n  ERROR: {e}\n")
        sys.exit(1)