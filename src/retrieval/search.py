
def search_documents(vector_store, question: str, k: int = 3):
    """Find the most relevant document chunks for a question."""
    if not question.strip():
        return []

    return vector_store.similarity_search(
        query=question,
        k=k,
    )


