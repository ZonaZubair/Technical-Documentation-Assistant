import pytest
from langchain_core.documents import Document

import src.chains.qa_chain as qa_module


class FakeChain:
    def invoke(self, inputs):
        assert "context" in inputs
        assert "question" in inputs
        return "Run streamlit run app.py to start the application."


def test_answer_question_returns_answer_and_sources(monkeypatch):
    documents = [
        Document(
            page_content="Run streamlit run app.py to start the application.",
            metadata={"source": "guide.md"},
        )
    ]

    monkeypatch.setattr(
        qa_module,
        "search_documents",
        lambda vector_store, question, k=3: documents,
    )
    monkeypatch.setattr(
        qa_module,
        "create_qa_chain",
        lambda: FakeChain(),
    )

    result = qa_module.answer_question(
        question="How do I start the application?",
        vector_store=object(),
    )

    assert "streamlit run app.py" in result["answer"]
    assert result["sources"] == ["guide.md"]


def test_answer_question_handles_no_results(monkeypatch):
    monkeypatch.setattr(
        qa_module,
        "search_documents",
        lambda vector_store, question, k=3: [],
    )

    result = qa_module.answer_question(
        question="What database is used?",
        vector_store=object(),
    )

    assert "couldn't find relevant information" in result["answer"]
    assert result["sources"] == []


def test_answer_question_rejects_empty_question():
    with pytest.raises(ValueError, match="Question cannot be empty"):
        qa_module.answer_question(
            question="   ",
            vector_store=object(),
        )