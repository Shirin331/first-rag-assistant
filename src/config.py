"""Central configuration for the RAG assistant.

All tunable settings live here so you can experiment in one place
instead of hunting through the code.
"""
import os
from dotenv import load_dotenv

# Load variables from a local .env file (your API key lives there).
load_dotenv()

# --- Paths ---
DATA_DIR = "data"                 # put your PDF manuals in here
CHROMA_DIR = "storage/chroma"     # persisted vector store (auto-created)
COLLECTION_NAME = "manuals"

# --- Models ---
# Multilingual embedding model. This matters: the manuals are in German,
# so an English-only embedder would retrieve poorly. Runs locally, no cost.
EMBED_MODEL = "intfloat/multilingual-e5-base"

# LLM via API. Default: OpenAI GPT-4o-mini (cheap and good enough here).
# Put OPENAI_API_KEY in your .env file. To use Anthropic instead, see README.
LLM_MODEL = "gpt-4o-mini"

# --- Chunking (Phase 2: tune these to improve answer quality) ---
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

# --- Retrieval ---
TOP_K = 4   # how many chunks to feed the LLM per question
