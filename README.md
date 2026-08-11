# 🔧 Wartungsassistent (RAG)

Ein KI-Assistent, der Fragen zu technischen Handbüchern und Wartungsdokumenten
beantwortet – und dabei **jede Antwort mit der Quelle belegt** (Dokument + Seite).
Umgesetzt als Retrieval-Augmented-Generation-Pipeline (RAG) mit semantischer Suche.

> Motivation: In Wartung und Inspektion steckt Wissen verstreut über hunderte
> Seiten Dokumentation. Dieser Assistent macht es in Sekunden durchsuchbar und
> beantwortet Fragen in natürlicher Sprache – mit nachvollziehbaren Quellen statt
> erfundener Antworten.

## Funktionen

- **Semantische Suche** über beliebig viele PDF-Handbücher
- **Quellenangabe** zu jeder Antwort (Dateiname + Seitenzahl)
- **Mehrsprachig** – nutzt ein multilinguales Embedding-Modell, damit auch
  deutschsprachige Dokumente zuverlässig gefunden werden
- **Lokaler Vektorspeicher** (Chroma) – einmal indexieren, danach schnell abfragen
- **Einfache Chat-Oberfläche** (Streamlit)

## Tech-Stack

| Baustein        | Wahl                                   |
|-----------------|----------------------------------------|
| Framework       | LlamaIndex                             |
| Embeddings      | `intfloat/multilingual-e5-base` (lokal)|
| Vektorspeicher  | ChromaDB (lokal, persistent)           |
| LLM             | OpenAI GPT-4o-mini (per API)           |
| Oberfläche      | Streamlit                              |

## Schnellstart

```bash
# 1. Repo klonen und ins Verzeichnis wechseln
git clone https://github.com/<dein-name>/psi-rag-assistant.git
cd psi-rag-assistant

# 2. Virtuelle Umgebung anlegen und aktivieren
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. API-Key hinterlegen
cp .env.example .env             # danach .env öffnen und Key eintragen

# 5. Setup testen (Phase 0)
python scripts/hello_llm.py
```

## Nutzung

```bash
# PDF-Handbücher in den Ordner data/ legen, dann Index bauen:
python -m src.ingest

# Frage direkt im Terminal stellen:
python -m src.query "Wie wird der Sensor kalibriert?"

# Oder die Chat-Oberfläche starten:
streamlit run app.py
```

## Projektstruktur

```
psi-rag-assistant/
├── app.py              # Streamlit-Chatoberfläche (Phase 3)
├── src/
│   ├── config.py       # zentrale Einstellungen (Modelle, Chunking, Pfade)
│   ├── ingest.py       # PDFs laden, chunken, embedden, speichern (Phase 1)
│   └── query.py        # Frage beantworten inkl. Quellen (Phase 1–2)
├── scripts/
│   └── hello_llm.py    # Setup-Test (Phase 0)
├── data/               # hier kommen die PDF-Handbücher rein (nicht im Repo)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Roadmap / Status

- [x] Phase 0 – Setup & API-Test
- [x] Phase 1 – End-to-End-Pipeline (Laden → Embedden → Antworten)
- [ ] Phase 2 – Qualität & Quellen: Chunking optimieren, Testfragen-Set, Evaluation
- [ ] Phase 3 – Streamlit-UI verfeinern
- [ ] Phase 4 – Dockerisierung & Demo-Clip

## Hinweise

- Die `.env` mit dem API-Key ist bewusst **nicht** Teil des Repos (`.gitignore`).
- Handbücher im Ordner `data/` werden ebenfalls nicht eingecheckt, da sie oft
  urheberrechtlich geschützt sind.
- Codekommentare sind auf Englisch gehalten (üblicher Standard), Dokumentation
  und Oberfläche auf Deutsch.
