# Career Knowledge Assistant

## Überblick

Der Career Knowledge Assistant ist ein persönliches AI-Tool zur Unterstützung bei Bewerbungen und Karriereplanung.

Er nutzt lokale KI-Modelle und eigene Dokumente (CV, Stellenanzeigen), um Fragen zu beantworten, Jobs zu analysieren und Lebensläufe zu optimieren.

---

## Funktionen

### 1. CV Q&A
- Fragen zum eigenen Lebenslauf beantworten
- z. B. Skills, Erfahrung, Ausbildung

### 2. Job Analyse
- Vergleich von Lebenslauf und Stellenanzeige
- Matching Score (0–100%)
- Stärken & Lücken

### 3. CV Optimierung
- Lebenslauf wird auf Stellenanzeige angepasst
- ATS-freundliche Struktur

---

## Tech Stack

- Python
- Streamlit
- Ollama (lokales LLM)
- PDF Parsing (pypdf)
- Simple RAG Pipeline

---

## Architektur

```
PDF → Text → Chunking → Suche → Prompt → LLM → Antwort
```

---

## Ziel

Dieses Projekt dient dazu:
- praktische AI-Erfahrung zu sammeln
- RAG-Systeme zu verstehen
- ein echtes Portfolio-Projekt zu bauen

---

## Status

🚧 In aktiver Entwicklung