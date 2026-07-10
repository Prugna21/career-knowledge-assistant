# 🧭 CareerPilot AI

> **AI-powered career copilot for CV intelligence, job matching and application tracking.**

## Demo

> Upload your CV → paste a job → get instant insights

* CV Match Score (0–100)
* AI-powered job analysis
* Semantic CV search (RAG-style)
* Application tracking system

## Key Features

### Smart CV Intelligence

Upload your CV (PDF) and interact with it like a knowledge base:

* Ask questions about your experience
* Retrieve relevant CV sections using semantic search
* Get structured AI answers

### Job Matching Engine

* Paste any job description
* AI compares it with your CV
* Detects skill gaps and strengths
* Generates structured feedback

### Match Score (0–100)

* Embedding-based similarity scoring
* Cosine similarity via SentenceTransformers
* Human-readable explanation of fit

### Application Tracker

* Save job applications
* View history in dashboard
* Track match scores over time
* Delete entries easily

## How It Works

```
 CV Upload (PDF)
        ↓
 Text Extraction (pypdf)
        ↓
 Chunking (semantic segments)
        ↓
 Embeddings (SentenceTransformers)
        ↓
 Semantic Search (Top-K retrieval)
        ↓
 LLM (Ollama / local model)
        ↓
 Insights / Answers / Analysis
        ↓
 Match Score Engine (0–100)
```

## Tech Stack

* Python
* Streamlit (UI)
* SentenceTransformers (Embeddings)
* NumPy (Similarity computation)
* Ollama (Local LLM) -- needed!
* pypdf (PDF parsing)
* Requests (API communication)
* ReportLab (PDF export)
* LangChain Text Splitters (optional)


## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app/app_ui.py
```


## Requirements

```text
streamlit
sentence-transformers
numpy
pypdf
requests
reportlab
langchain-text-splitters
```


## Architecture

```
┌──────────────┐
│  CV Upload   │
└──────┬───────┘
       ↓
┌──────────────┐
│ Text Extract │
└──────┬───────┘
       ↓
┌──────────────┐
│ Chunking     │
└──────┬───────┘
       ↓
┌──────────────┐
│ Embeddings   │
└──────┬───────┘
       ↓
┌──────────────┐
│ Semantic     │
│ Search       │
└──────┬───────┘
       ↓
┌──────────────┐
│ LLM (Ollama) │
└──────┬───────┘
       ↓
┌──────────────┐
│ Insights     │
└──────────────┘
```

## Privacy First

* CV uploaded by user (no static files)
* No persistent CV storage
* In-memory processing only
* Safe for cloud deployment (Streamlit Cloud)


## Current Status

✔ CV Upload System
✔ Semantic CV Intelligence
✔ Job Matching Engine
✔ AI Job Analysis
✔ Match Score (0–100)
✔ Application Tracking


## Project Vision

* Retrieval-Augmented Generation (RAG)
* Semantic search over personal documents
* Real-world job matching logic
* LLM-based reasoning workflows
