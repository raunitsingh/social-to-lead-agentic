from langchain.schema import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import LLM_PROVIDER, LLM_MODEL, logger
from rag.retriever import retrieve


# ── Load the correct LLM based on provider ────────────────────────────────────
def _load_llm() -> BaseChatModel:
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq
        from config import GROQ_API_KEY
        return ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        from config import ANTHROPIC_API_KEY
        return ChatAnthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        from config import OPENAI_API_KEY
        return ChatOpenAI(model=LLM_MODEL, api_key=OPENAI_API_KEY, temperature=0.2)

    if LLM_PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        from config import GOOGLE_API_KEY
        return ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2)

    raise ValueError(f"Unsupported provider: {LLM_PROVIDER}")


# ── Prompt template ───────────────────────────────────────────────────────────
_RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful sales assistant for AutoStream, \
an AI-powered video editing SaaS for content creators.

Answer the user's question using ONLY the context provided below.
Be concise, friendly, and accurate. If the answer is not in the context, \
say "I don't have that information — please contact support@autostream.io".

Context:
{context}
"""),
    ("human", "{question}"),
])


# ── Build the RAG chain ───────────────────────────────────────────────────────
def build_rag_chain(retriever: BaseRetriever):
    """
    Returns a callable chain:
        chain.invoke({"question": "..."}) -> str answer
    """
    llm    = _load_llm()
    parser = StrOutputParser()

    def format_context(inputs: dict) -> dict:
        question = inputs["question"]
        context  = retrieve(retriever, question)
        return {"context": context, "question": question}

    chain = (
        RunnablePassthrough()
        | format_context
        | _RAG_PROMPT
        | llm
        | parser
    )

    logger.info(f"RAG chain ready — provider={LLM_PROVIDER}, model={LLM_MODEL}")
    return chain


if __name__ == "__main__":
    from config import KB_PATH, VECTORSTORE_PATH, RAG_TOP_K
    from rag.loader import load_kb
    from rag.vectorstore import get_vectorstore
    from rag.retriever import get_retriever

    print("\nBuilding RAG chain...\n")
    docs        = load_kb(KB_PATH)
    vectorstore = get_vectorstore(docs, VECTORSTORE_PATH)
    retriever   = get_retriever(vectorstore, top_k=RAG_TOP_K)
    chain       = build_rag_chain(retriever)

    test_questions = [
        "What is the price of the Pro plan?",
        "Does the Basic plan include AI captions?",
        "What is the refund policy?",
        "Can I get 24/7 support on the Basic plan?",
    ]

    print("── RAG Chain Test ───────────────────────────────────────\n")
    for q in test_questions:
        print(f"Q: {q}")
        answer = chain.invoke({"question": q})
        print(f"A: {answer}\n")