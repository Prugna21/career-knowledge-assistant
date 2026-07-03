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
# UI
# -------------------
st.title("CareerPilot AI 🧭")
st.caption("Your AI-powered career assistant.")


mode = st.selectbox(
    "Modus wählen",
    ["CV Frage", "Job Analyse"]
)

# -------------------
# CV LOAD
# -------------------
cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

if not pdf_files:
    st.error("Kein CV gefunden im data/cv Ordner")
    st.stop()

selected_cv = st.selectbox(
    "Wähle deinen CV",
    pdf_files,
    format_func=lambda x: x.name
)

cv_text = read_pdf(selected_cv)
chunks = split_text(cv_text)


@st.cache_resource
def get_embeddings(chunks):
    return build_index(tuple(chunks))


chunk_embeddings = get_embeddings(chunks)


# Cache embeddings (wichtig für Performance)
@st.cache_resource
def get_embeddings(chunks):
    return build_index(tuple(chunks))


chunk_embeddings = get_embeddings(chunks)

# -------------------
# SIDEBAR
# -------------------
with st.sidebar:
    st.header("📋 Applications")

    if st.button("Bewerbungen anzeigen"):
        apps = load_applications()

        if not apps:
            st.info("No applications yet.")
        else:
            for i, app in enumerate(reversed(apps), start=1):
                with st.expander(f"Application {i} - Score: {app.get('match_score', 'N/A')}"):
                    st.write(f"**Date:** {app.get('date')}")
                    st.write(f"**Match Score:** {app.get('match_score', 'N/A')}")
                    st.write("**Job Text:**")
                    st.write(app.get("job_text", ""))

# -------------------
# MODE 1: CV QUESTION
# -------------------
if mode == "CV Frage":
    question = st.text_input("Frage zu deinem Lebenslauf")

    if st.button("Antwort generieren"):
        if question.strip():
            relevant_chunks = search(
                question,
                chunks,
                chunk_embeddings,
                top_k=4
            )

            context = "\n\n".join(relevant_chunks)

            prompt = f"""
Du bist ein präziser Karriere-Experte.

Nutze ausschliesslich den Kontext.
Wenn etwas fehlt, sage: "nicht im Lebenslauf enthalten".

Antworte klar in Bullet Points.

KONTEXT:
{context}

FRAGE:
{question}
"""

            st.write(ask_llm(prompt))


# -------------------
# MODE 2: JOB ANALYSIS
# -------------------
elif mode == "Job Analyse":
    job_text = st.text_area("Stellenanzeige einfügen")

    # SESSION STATE
    if "match_result" not in st.session_state:
        st.session_state.match_result = None

    if st.button("Analyse starten"):
        if job_text.strip():
            result = ask_llm(build_job_prompt(cv_text, job_text))
            st.write(result)

    if st.button("Match Score berechnen"):
        if job_text.strip():
            score, explanation = compute_match_score(cv_text, job_text)
            st.session_state.match_result = (score, explanation)

    if st.session_state.match_result:
        score, explanation = st.session_state.match_result

        st.metric("CV Match Score", f"{score}/100")
        st.write(explanation)

    if st.button("Diese Bewerbung speichern"):
        if job_text.strip():

            score = None
            if st.session_state.match_result:
                score = st.session_state.match_result[0]

            save_application({
                "date": str(datetime.now()),
                "job_text": job_text,
                "match_score": score
            })

            st.success("Bewerbung gespeichert")