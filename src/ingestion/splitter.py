
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """Split loaded documents into smaller, searchable chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        add_start_index=True,
    )

    return splitter.split_documents(documents)
