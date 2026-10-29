
import sys

from dotenv import load_dotenv

from src.ingestion.pipeline import ingest_files
from src.retrieval.vector_store import create_vector_store
from src.chains.qa_chain import answer_question


load_dotenv()


def main():
    try:
        chunks = ingest_files(["data/sample_troubleshooting.md"])

        if not chunks:
            print("Error: No readable text was found in the sample document.")
            sys.exit(1)

        vector_store = create_vector_store(chunks)

        result = answer_question(
            question="How do I start the application?",
            vector_store=vector_store,
        )

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print(f"- {source}")

    except Exception as error:
        error_text = str(error).lower()

        if any(
            phrase in error_text
            for phrase in (
                "failed to connect",
                "connection refused",
                "could not connect",
                "connection error",
            )
        ):
            print(
                "\nError: Could not connect to Ollama. "
                "Make sure Ollama is running and the required models "
                "are installed."
            )
        else:
            print("\nError: The local question-answering test failed.")

        print(f"Technical details: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
