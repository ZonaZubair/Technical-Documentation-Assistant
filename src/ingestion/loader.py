
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}


def load_document(file_path: str | Path):
    """Load a supported document and return LangChain Document objects."""
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))
    else:
        loader = TextLoader(
            str(path),
            encoding="utf-8",
            autodetect_encoding=True,
        )

    documents = loader.load()

    for document in documents:
        document.metadata["source"] = path.name

    return documents


def load_documents(file_paths: list[str | Path]):
    """Load multiple documents and combine their pages or text."""
    documents = []

    for file_path in file_paths:
        documents.extend(load_document(file_path))

    return documents
