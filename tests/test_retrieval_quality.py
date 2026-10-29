from dotenv import load_dotenv

from src.ingestion.pipeline import ingest_files
from src.retrieval.search import search_documents
from src.retrieval.vector_store import create_vector_store

load_dotenv(".env")


def test_faiss_question_retrieves_relevant_passage():
    chunks = ingest_files(["data/sample_project_guide.md"])
    vector_store = create_vector_store(chunks)

    results = search_documents(
        vector_store,
        "Which vector database does this project use?",
        k=3,
    )

    retrieved_text = "\n".join(
        document.page_content for document in results
    ).lower()

    assert "faiss" in retrieved_text