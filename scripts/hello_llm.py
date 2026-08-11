"""Phase 0 smoke test: confirm your LLM API key works before building anything.

    python scripts/hello_llm.py

If you see a short German sentence printed, your setup is good to go.
"""
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv()

llm = OpenAI(model="gpt-4o-mini")
print(llm.complete("Antworte mit genau einem kurzen Satz: Das Setup funktioniert."))
