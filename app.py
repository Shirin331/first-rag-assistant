"""Phase 3: minimal Streamlit chat UI for the manual assistant.

Run from the repo root:
    streamlit run app.py
"""
import streamlit as st

from src.query import load_query_engine, format_sources

st.set_page_config(page_title="Wartungsassistent (RAG)", page_icon="🔧")
st.title("🔧 Wartungsassistent")
st.caption("Fragen zu den technischen Handbüchern – beantwortet mit Quellenangabe.")


@st.cache_resource
def get_engine():
    # Cached so the model + index load only once per session, not per question.
    return load_query_engine()


engine = get_engine()

question = st.text_input(
    "Ihre Frage:",
    placeholder="z. B. Wie wird der Sensor kalibriert?",
)

if question:
    with st.spinner("Suche in den Handbüchern ..."):
        response = engine.query(question)
    st.markdown("### Antwort")
    st.write(str(response))
    st.markdown("### Quellen")
    st.text(format_sources(response))
