"""Phase 1: build the search index from your PDF manuals.

Reads every PDF in DATA_DIR, splits the text into chunks, creates
multilingual embeddings, and stores them in a local Chroma database so
you don't have to re-embed on every run.

Run once (and again whenever you add new manuals):
    python -m src.ingest
"""
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from src import config


def build_index():
    # 1. Load PDFs. SimpleDirectoryReader creates one document per page and
    #    attaches metadata (file_name + page_label) we reuse for citations.
    docs = SimpleDirectoryReader(config.DATA_DIR).load_data()
    if not docs:
        raise SystemExit(
            f"No documents found in '{config.DATA_DIR}/'. "
            "Drop a few PDF manuals in there first."
        )
    print(f"Loaded {len(docs)} pages from {config.DATA_DIR}/")

    # 2. Configure the embedding model + chunking globally.
    Settings.embed_model = HuggingFaceEmbedding(model_name=config.EMBED_MODEL)
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    # 3. Set up a persistent Chroma vector store.
    client = chromadb.PersistentClient(path=config.CHROMA_DIR)
    collection = client.get_or_create_collection(config.COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Build + persist the index.
    print("Embedding and indexing... (first run downloads the embedding model)")
    VectorStoreIndex.from_documents(docs, storage_context=storage_context)
    print(f"Done. Index stored in '{config.CHROMA_DIR}/'.")


if __name__ == "__main__":
    build_index()
