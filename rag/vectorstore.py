from pathlib import Path
from typing import List

from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Free local embedding model — downloads once (~90MB), runs offline after
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Return the embedding model (downloaded on first call)."""
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore(docs: List[Document], save_path: Path) -> FAISS:
    """
    Embed all documents and save FAISS index to disk.
    Call this once (or when KB changes).
    """
    print(f"  Building FAISS index from {len(docs)} chunks...")
    embeddings = _get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    save_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(save_path))
    print(f"  Index saved to {save_path}")
    return vectorstore


def load_vectorstore(save_path: Path) -> FAISS:
    """Load an existing FAISS index from disk."""
    embeddings = _get_embeddings()
    return FAISS.load_local(
        str(save_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def get_vectorstore(docs: List[Document], save_path: Path) -> FAISS:
    """
    Smart loader:
      - If index exists on disk → load it (fast)
      - Otherwise → build and save it
    """
    index_file = save_path / "index.faiss"
    if index_file.exists():
        print(f"  Loading existing FAISS index from {save_path}")
        return load_vectorstore(save_path)
    else:
        return build_vectorstore(docs, save_path)


if __name__ == "__main__":
    from config import KB_PATH, VECTORSTORE_PATH
    from rag.loader import load_kb

    docs = load_kb(KB_PATH)
    vs   = get_vectorstore(docs, VECTORSTORE_PATH)
    print(f"\nVector store ready. Total vectors: {vs.index.ntotal}")