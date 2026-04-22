from langchain_community.vectorstores import FAISS
from langchain.schema import BaseRetriever


def get_retriever(vectorstore: FAISS, top_k: int = 4) -> BaseRetriever:
    """
    Return a retriever that fetches the top-k most relevant chunks.

    Args:
        vectorstore : the loaded FAISS index
        top_k       : number of chunks to retrieve (default from config)
    """
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )


def retrieve(retriever: BaseRetriever, query: str) -> str:
    """
    Run a query and return retrieved chunks as a single formatted string
    ready to be injected into the LLM prompt.
    """
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information found in the knowledge base."

    chunks = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        chunks.append(f"[{i}] ({source})\n{doc.page_content}")

    return "\n\n".join(chunks)


if __name__ == "__main__":
    from config import KB_PATH, VECTORSTORE_PATH, RAG_TOP_K
    from rag.loader import load_kb
    from rag.vectorstore import get_vectorstore

    docs        = load_kb(KB_PATH)
    vectorstore = get_vectorstore(docs, VECTORSTORE_PATH)
    retriever   = get_retriever(vectorstore, top_k=RAG_TOP_K)

    test_queries = [
        "What is the price of the Pro plan?",
        "Does the Basic plan support 4K?",
        "What is the refund policy?",
        "Is 24/7 support available?",
        "Does AutoStream support AI captions?",
    ]

    print("\n── Retrieval Test ───────────────────────────────────────\n")
    for query in test_queries:
        print(f"Q: {query}")
        result = retrieve(retriever, query)
        # Print just first chunk for brevity
        first_chunk = result.split("\n\n")[0]
        print(f"A: {first_chunk[:120]}...")
        print()