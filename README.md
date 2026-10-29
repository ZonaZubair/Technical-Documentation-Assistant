
# Technical Documentation Companion

A Python application for exploring technical documentation
and answering questions using retrieval-augmented generation (RAG).

## Planned Features

- Upload PDF, Markdown, and plain-text documentation
- Load and split documents using LangChain
- Generate embeddings and store them in a FAISS vector store
- Retrieve relevant passages to answer technical questions
- Maintain conversation context for follow-up questions
- Display source references for generated answers
- Explore LangChain chains, prompts, and tool use

## Technology Stack

- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS
- PyPDF

## Local Setup

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`.
5. Add your OpenAI API key to `.env`.
6. Start the application:

   ```bash
   streamlit run app.py
   ```

## Project Status

The initial user interface is under development.
Document ingestion, retrieval, and question answering
will be implemented in subsequent stages.

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
