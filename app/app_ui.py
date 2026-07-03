import streamlit as st
from pathlib import Path
from datetime import datetime
from pdf_reader import read_pdf
from text_splitter import split_text
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from app_state import save_application, load_applications
from semantic_search import build_index, search
from match_engine import compute_match_score


# -------------------
# CV laden
# -------------------
cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

if not pdf_files:
    st.error("Kein CV gefunden")
    st.stop()

cv_text = read_pdf(pdf_files[0])
chunks = split_text(cv_text)
@st.cache_resource
def get_embeddings(chunks):
    return build_index(chunks)

chunk_embeddings = get_embeddings(chunks)


# -------------------
# UI
# -------------------
st.title("CareerPilot AI 🧭")
st.caption("Your AI-powered career assistant.")

mode = st.selectbox(
    "Modus wählen",
    ["CV Frage", "Job Analyse"]
)


# -------------------
# SIDEBAR
# -------------------
with st.sidebar:
    if st.button("📋 Bewerbungen anzeigen"):
        apps = load_applications()
        st.write(apps)


# -------------------
# MODE 1
# -------------------
if mode == "CV Frage":
    question = st.text_input("Frage zu deinem Lebenslauf")

    if st.button("Antwort generieren"):
        if question.strip():
            relevant_chunks = search(question, chunks, chunk_embeddings, top_k=4)
            context = "\n\n".join(relevant_chunks)

            prompt = f"""
Du bist ein präziser Karriere-Experte.

Arbeite nur mit dem gegebenen Kontext.
Wenn etwas nicht vorhanden ist, sage "nicht im Lebenslauf enthalten".

Gib strukturierte, klare Bullet Points.

KONTEXT:
{context}

FRAGE:
{question}
"""

            st.write(ask_llm(prompt))


# -------------------
# MODE 2
# -------------------
elif mode == "Job Analyse":
    job_text = st.text_area("Stellenanzeige einfügen")

    if st.button("Analyse starten"):
        if job_text.strip():
            st.write(ask_llm(build_job_prompt(cv_text, job_text)))

    if st.button("Match Score berechnen"):
        if job_text.strip():
            score, explanation = compute_match_score(cv_text, job_text)
            st.metric("CV Match Score", f"{score}/100")
            st.write(explanation)

    if st.button("Diese Bewerbung speichern"):
        if job_text.strip():
            save_application({
                "date": str(datetime.now()),
                "job_text": job_text
            })
            st.success("Bewerbung gespeichert")