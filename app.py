
import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.chains.qa_chain import answer_question
from src.ingestion.pipeline import ingest_files
from src.retrieval.vector_store import create_vector_store


load_dotenv()


def friendly_error_message(error):
    """Return an actionable message for common local AI errors."""
    error_text = str(error).lower()

    if any(
        phrase in error_text
        for phrase in (
            "connection refused",
            "connection error",
            "failed to connect",
            "could not connect",
            "connection reset",
        )
    ):
        return (
            "Could not connect to Ollama. Make sure Ollama is running "
            "and check its available models with `ollama list`."
        )

    if "model" in error_text and any(
        phrase in error_text
        for phrase in ("not found", "pull model", "does not exist")
    ):
        return (
            "The requested Ollama model may not be installed. Check "
            "your model settings and run `ollama list`. Download a "
            "missing model with `ollama pull MODEL_NAME`."
        )

    return (
        "The operation failed. Review the technical details below "
        "to help identify the problem."
    )


def make_unique_filename(filename, used_names):
    """Avoid overwriting uploads that share the same filename."""
    original_name = Path(filename).name
    path = Path(original_name)

    candidate = original_name
    counter = 2

    while candidate.casefold() in used_names:
        candidate = f"{path.stem} ({counter}){path.suffix}"
        counter += 1

    used_names.add(candidate.casefold())
    return candidate


st.set_page_config(
    page_title="Technical Documentation Companion",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Technical Documentation Companion")
st.caption(
    "Ask questions about your technical documentation using local AI."
)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Document Library")

    st.caption(
        "Documents are processed locally using Ollama embeddings and FAISS."
    )

    uploaded_files = st.file_uploader(
        "Upload technical documents",
        type=["pdf", "md", "txt"],
        accept_multiple_files=True,
        help="Upload PDF, Markdown, or plain-text documentation.",
    )

    process_clicked = st.button(
        "Process Documents",
        type="primary",
        disabled=not uploaded_files,
        use_container_width=True,
    )

    if process_clicked and uploaded_files:
        try:
            with st.spinner(
                "Loading documents and building the search index..."
            ):
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_paths = []
                    used_names = set()

                    for uploaded_file in uploaded_files:
                        unique_name = make_unique_filename(
                            uploaded_file.name,
                            used_names,
                        )

                        file_path = Path(temp_dir) / unique_name
                        file_path.write_bytes(uploaded_file.getvalue())
                        file_paths.append(file_path)

                    chunks = ingest_files(file_paths)

                    # Ignore empty chunks, such as pages without readable text.
                    chunks = [
                        chunk
                        for chunk in chunks
                        if chunk.page_content.strip()
                    ]

                    if not chunks:
                        st.error(
                            "No readable text was found. Check that your "
                            "documents contain extractable text. Scanned "
                            "PDFs may require OCR."
                        )
                    else:
                        # Build the new index before changing the current one.
                        new_vector_store = create_vector_store(chunks)

                        # Update session state only after successful indexing.
                        st.session_state.vector_store = new_vector_store

                        st.session_state.indexed_files = []
                        used_names_for_display = set()

                        for uploaded_file in uploaded_files:
                            st.session_state.indexed_files.append(
                                make_unique_filename(
                                    uploaded_file.name,
                                    used_names_for_display,
                                )
                            )

                        st.session_state.messages = []

                        # Reconstruct names consistently for duplicate uploads.
                        st.session_state.indexed_files = []
                        used_names_for_display = set()

                        for uploaded_file in uploaded_files:
                            st.session_state.indexed_files.append(
                                make_unique_filename(
                                    uploaded_file.name,
                                    used_names_for_display,
                                )
                            )

                        st.session_state.messages = []

                        st.success(
                            f"Indexed {len(uploaded_files)} document(s) "
                            f"into {len(chunks)} searchable chunk(s)."
                        )

        except Exception as error:
            st.error(friendly_error_message(error))
            st.caption(f"Technical details: {error}")

    if st.session_state.indexed_files:
        st.subheader("Indexed Documents")

        for filename in st.session_state.indexed_files:
            st.write(f"📄 {filename}")

        if st.button("Clear Documents and Chat", use_container_width=True):
            st.session_state.vector_store = None
            st.session_state.indexed_files = []
            st.session_state.messages = []
            st.rerun()

    st.divider()

    st.caption(
        f"Chat model: {os.getenv('OLLAMA_CHAT_MODEL', 'llama3.2:3b')}"
    )
    st.caption("Local development version")


if st.session_state.vector_store is None:
    st.info(
        "Upload your technical documents in the sidebar and select "
        "**Process Documents** to get started."
    )
else:
    st.subheader("Ask Your Documentation")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                st.caption("Sources: " + ", ".join(message["sources"]))

    question = st.chat_input("Ask a question about your documents...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        previous_history = st.session_state.messages.copy()

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        try:
            with st.chat_message("assistant"):
                with st.spinner(
                    "Searching your documents and generating an answer..."
                ):
                    result = answer_question(
                        question=question,
                        vector_store=st.session_state.vector_store,
                        chat_history=previous_history,
                    )

                st.markdown(result["answer"])

                if result["sources"]:
                    st.caption("Sources: " + ", ".join(result["sources"]))

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                }
            )

        except Exception as error:
            error_message = friendly_error_message(error)

            with st.chat_message("assistant"):
                st.error(error_message)
                st.caption(f"Technical details: {error}")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                }
            )
