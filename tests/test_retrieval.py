
from src.retrieval.search import search_documents


class FakeVectorStore:
    def similarity_search(self, query, k=3):
        return [
            {
                "query": query,
                "k": k,
            }
        ]


def test_search_documents_returns_results():
    store = FakeVectorStore()

    results = search_documents(
        store,
        "How do I run the application?",
    )

    assert len(results) == 1
    assert results[0]["query"] == "How do I run the application?"
    assert results[0]["k"] == 3


def test_search_documents_skips_empty_question():
    results = search_documents(FakeVectorStore(), "   ")

    assert results == []
