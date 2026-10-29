from pathlib import Path

import pytest

from src.ingestion.loader import load_document
from src.ingestion.splitter import split_documents


def test_load_markdown_document(tmp_path):
    file_path = tmp_path / "guide.md"
    file_path.write_text(
        "# Setup\nRun streamlit run app.py",
        encoding="utf-8",
    )

    documents = load_document(file_path)

    assert len(documents) == 1
    assert "streamlit run app.py" in documents[0].page_content
    assert documents[0].metadata["source"] == "guide.md"


def test_loader_rejects_unsupported_file(tmp_path):
    file_path = tmp_path / "notes.csv"
    file_path.write_text("name,value", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(file_path)


def test_split_documents_creates_multiple_chunks():
    from langchain_core.documents import Document

    document = Document(
        page_content=("Python documentation explains setup and testing. " * 100),
        metadata={"source": "guide.md"},
    )

    chunks = split_documents([document])

    assert len(chunks) > 1
    assert all(chunk.page_content for chunk in chunks)
    assert all(chunk.metadata["source"] == "guide.md" for chunk in chunks)
    assert all("start_index" in chunk.metadata for chunk in chunks)