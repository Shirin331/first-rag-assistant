"""Phase 1-2: answer a question over the indexed manuals, with sources.

Loads the persisted Chroma index and runs a retrieval-augmented query.
Every answer comes back together with the manuals and page numbers it
was based on -- that citation step is what turns a toy into a showcase.

Quick test from the terminal:
    python -m src.query "Wie wird der Sensor kalibriert?"
"""
import sys

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from src import config


def load_query_engine():
    # The embedding model MUST match the one used during ingest.
    Settings.embed_model = HuggingFaceEmbedding(model_name=config.EMBED_MODEL)
    Settings.llm = OpenAI(model=config.LLM_MODEL)

    client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    collection = client.get_or_create_collection(config.COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=collection)

    index = VectorStoreIndex.from_vector_store(vector_store)
    return index.as_query_engine(similarity_top_k=config.TOP_K)


def format_sources(response) -> str:
    """Turn the retrieved chunks into a readable citation list."""
    seen = set()
    lines = []
    for node in response.source_nodes:
        meta = node.metadata
        name = meta.get("file_name", "unbekannt")
        page = meta.get("page_label", "?")
        key = (name, page)
        if key in seen:      # avoid listing the same page twice
            continue
        seen.add(key)
        lines.append(f"  - {name}, S. {page}")
    return "\n".join(lines) if lines else "  (keine Quellen gefunden)"


def ask(question: str):
    engine = load_query_engine()
    response = engine.query(question)
    print("\nAntwort:\n" + str(response))
    print("\nQuellen:\n" + format_sources(response))
    return response


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Welche Wartung ist erforderlich?"
    ask(q)
