
import os

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


def create_vector_store(chunks):
    """Create a FAISS vector store using local Ollama embeddings."""
    if not chunks:
        raise ValueError(
            "Cannot create a vector store without document chunks."
        )

    embeddings = OllamaEmbeddings(
        model=os.getenv(
            "OLLAMA_EMBEDDING_MODEL",
            "nomic-embed-text",
        )
    )

    return FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )
