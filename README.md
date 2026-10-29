# Technical Documentation Companion

A local AI application that helps you search technical documents and get answers to your questions. It uses RAG (Retrieval-Augmented Generation) to find relevant information in your documents and generate answers with source references.

## Features

- Upload PDF, Markdown, and plain-text documents.
- Extract and split document content into smaller chunks.
- Create embeddings and store them in a FAISS vector store.
- Ask questions about uploaded documents.
- Retrieve relevant passages to help generate answers.
- View source documents used to answer questions.
- Run the AI models locally using Ollama, without a paid API.

## Technology Stack

- **Python** for application logic
- **Streamlit** for the user interface
- **LangChain** for document processing and question answering
- **Ollama** for running local AI models
- **FAISS** for storing and searching document embeddings
- **PyPDF** for reading PDF documents

## Requirements

- Python 3.11 or a compatible Python version
- [Ollama](https://ollama.com/)
- Git (optional, for cloning the repository)

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ZonaZubair/Technical-Documentation-Assistant
cd technical-documentation-assistant
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install the local AI models

Make sure Ollama is installed and running. Download the required models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

The first model generates answers, while the second creates embeddings for document search.

### 5. Configure the environment

Create a `.env` file by copying `.env.example`:

```powershell
Copy-Item .env.example .env
```

Check that the configuration contains the required model names:

```dotenv
OLLAMA_CHAT_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

No paid API key is required for local use.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Running Tests

Run the test suite with:

```bash
python -m pytest tests -v
```

The tests cover document loading, text splitting, retrieval, question answering, and retrieval quality.

## Supported Documents

The current document loader supports PDF, Markdown (`.md`), and plain-text (`.txt`) files.

Some PDFs, especially scanned documents and files with complex layouts, may require additional text extraction or OCR support. Word documents, spreadsheets, and image files are not currently supported by the document loader.

## Project Structure

```text
technical-documentation-assistant/
├── data/                   # Sample documents
├── src/
│   ├── chains/              # Question-answering logic
│   ├── ingestion/           # Document loading and splitting
│   ├── retrieval/           # Embeddings and document search
│   └── tools/
├── tests/                  # Automated tests
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Example configuration
└── README.md
```

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Ollama Documentation](https://docs.ollama.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
