from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import logger

EMBED_MODEL = "all-MiniLM-L6-v2"

def _embeddings():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def get_vectorstore(docs, save_path):
    save_path = str(save_path)
    logger.info(f"Building Chroma index from {len(docs)} chunks...")
    vs = Chroma.from_documents(docs, _embeddings(), persist_directory=save_path)
    logger.info("Chroma index ready.")
    return vs

def build_vectorstore(docs, save_path):
    return get_vectorstore(docs, save_path)
