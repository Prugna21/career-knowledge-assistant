# Career Knowledge Assistant

AI-powered career assistant for CV analysis, job matching, CV optimization and match scoring.

---

## Features

### CV Intelligence
- Ask questions about your CV
- Semantic search using embeddings
- Context-aware AI answers

### Job Analysis
- Analyze job descriptions vs CV
- AI-generated structured feedback

### CV Match Score
- Calculates similarity between CV and job
- Score from 0–100
- Human-readable explanation of fit quality

### Application Tracking
- Save job applications
- View history in sidebar

---

## AI Architecture

```
PDF → Text → Chunking → Embeddings → Semantic Search → LLM
                               ↓
                      Match Score Engine
```

---

## Tech Stack

- Python
- Streamlit
- Sentence Transformers (Embeddings)
- Ollama / LLM API
- NumPy
- ReportLab (PDF export)

---

## How to run

```bash
pip install -r requirements.txt
streamlit run app/app_ui.py
```

---

## Project Structure

```
app/
  app_ui.py
semantic_search.py
match_engine.py
pdf_reader.py
text_splitter.py
ai_engine.py
job_analyzer.py
cv_optimizer.py
cv_exporter.py
app_state.py
```

---

## Current Status

✓ CV Intelligence
✓ Semantic Search
✓ Job Analysis
✓ CV Match Score
✓ Application Tracking

---

## Next Steps

See 'roadmap.md'