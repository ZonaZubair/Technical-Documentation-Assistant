
from pathlib import Path

from src.ingestion.loader import load_documents
from src.ingestion.splitter import split_documents


def ingest_files(file_paths: list[str | Path]):
    """Load files, split their contents, and return searchable chunks."""
    documents = load_documents(file_paths)
    chunks = split_documents(documents)

    return chunks
