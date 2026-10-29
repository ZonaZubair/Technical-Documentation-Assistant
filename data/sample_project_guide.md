# Technical Project Guide

## 1. Installation and Setup

This project uses Python 3.11 and a virtual environment to isolate its dependencies.
Before running the application, activate the virtual environment from the project root.

Install the required packages with:

python -m pip install -r requirements.txt

To verify the installed packages, run:

python -m pip check

## 2. Starting the Application

The user interface is built with Streamlit. Start the application from the project root:

streamlit run app.py

Streamlit prints a local URL in the terminal. Open that URL in your browser to access the application.
Upload a supported PDF, Markdown, or plain-text document, then select Process Documents.
After processing completes, enter a question in the chat input.

## 3. API and Application Structure

The application separates document ingestion, retrieval, and question answering into different modules.
The ingestion pipeline loads supported files and divides their contents into smaller text chunks.
The retrieval module searches the vector store for chunks relevant to the user's question.
The question-answering module sends the retrieved context and question to a local language model.

The main application entry point is app.py.
Document loading is implemented in src/ingestion/loader.py.
Text splitting is implemented in src/ingestion/splitter.py.
The ingestion pipeline is implemented in src/ingestion/pipeline.py.
Vector-store creation is implemented in src/retrieval/vector_store.py.
Similarity search is implemented in src/retrieval/search.py.
Question answering is implemented in src/chains/qa_chain.py.

## 4. Vector Database and Embeddings

This project uses FAISS as its local vector store. FAISS searches vector representations of document chunks.
The embedding model converts text into numerical vectors so that semantically related passages can be retrieved.

The configured embedding model is nomic-embed-text, which runs through Ollama.
The application creates embeddings from document chunks and stores them in a FAISS index.
The generated index is stored locally in the faiss_index directory when index persistence is used.

FAISS is not a relational database. It is used here for similarity search over vector embeddings.
The application does not require a hosted vector database or a paid embedding API.

## 5. Local Language Model

The default chat model is llama3.2:3b, served locally by Ollama.
Ollama must be installed and running, and the selected model must be available before questions can be answered.

The OLLAMA_CHAT_MODEL environment variable selects the chat model.
The OLLAMA_EMBEDDING_MODEL environment variable selects the embedding model.
These settings are stored in the local .env file.

The application uses a temperature of zero to encourage more consistent answers.
The language model is instructed to answer from retrieved documentation and to say when the supplied context does not contain the answer.

## 6. Supported Document Types

The application accepts PDF, Markdown, and plain-text files.
PDF files are loaded using PyPDFLoader.
Markdown and plain-text files are loaded using TextLoader with UTF-8 encoding and automatic encoding detection.

Each loaded document receives a source filename in its metadata.
The text splitter uses a chunk size of 800 characters and an overlap of 120 characters.
Overlapping chunks help preserve context when a relevant passage crosses a chunk boundary.

Unsupported file types should be rejected with a clear error message.
If a PDF contains scanned pages without extractable text, it may require OCR before its contents can be searched.

## 7. Common Issue: Missing Python Module

If Python reports that a module is missing, first confirm that the virtual environment is activated.
Then reinstall the project's dependencies with:

python -m pip install -r requirements.txt

Run the application from the project root so that Python can locate the src package.
If the error continues, check the exact module name in the error message and verify the relevant package is listed in requirements.txt.

## 8. Common Issue: Ollama Model Unavailable

If the application cannot connect to the local model, confirm that Ollama is installed and running.
Check available models with:

ollama list

If llama3.2:3b is missing, download it with:

ollama pull llama3.2:3b

If nomic-embed-text is missing, download it with:

ollama pull nomic-embed-text

The model names in the local .env file must match the names shown by Ollama.
Model downloads require an internet connection, but normal inference runs locally after the models are installed.

## 9. Common Issue: Poor or Missing Search Results

If the answer does not contain the expected information, verify that the document was uploaded and processed successfully.
Check that the file contains readable text and that the relevant information is present in the document.
Try asking a more specific question using terminology that appears in the documentation.

The retriever currently returns three relevant chunks by default.
Increasing the number of retrieved chunks can provide more context, but may also introduce unrelated passages.
The quality of the answer depends on document quality, chunking, retrieval relevance, and the language model.

## 10. Testing and Project Maintenance

Run the automated tests with:

python -m pytest tests -v

Tests should check document loading, text splitting, empty-question handling, retrieval behavior, and source attribution.
Tests should not require paid APIs or download a language model just to verify basic application logic.

Keep generated vector indexes, virtual environments, and local configuration files out of version control.
Commit sample documentation and automated tests so other developers can reproduce the basic workflow.
