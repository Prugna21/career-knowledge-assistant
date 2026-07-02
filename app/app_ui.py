import streamlit as st
from pathlib import Path

from pdf_reader import read_pdf
from text_splitter import split_text
from search import simple_search
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from cv_optimizer import build_cv_prompt

# CV laden
cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))
cv_text = read_pdf(pdf_files[0])
chunks = split_text(cv_text)

st.title("Career Knowledge Assistant")

mode = st.selectbox(
    "Modus wählen",
    [
        "CV Frage",
        "Job Analyse",
        "CV Optimieren"
    ]
)

# -------------------
# MODE 1
# -------------------
if mode == "CV Frage":
    question = st.text_input("Frage zu deinem Lebenslauf")

    if st.button("Antwort generieren"):
        relevant_chunks = simple_search(question, chunks)
        context = "\n\n".join(relevant_chunks)

        prompt = f"""
Du bist ein Karriere-Assistent.

Beantworte nur mit dem Kontext.

KONTEXT:
{context}

FRAGE:
{question}
"""

        answer = ask_llm(prompt)
        st.write(answer)

# -------------------
# MODE 2
# -------------------
elif mode == "Job Analyse":
    job_text = st.text_area("Stellenanzeige einfügen")

    if st.button("Analyse starten"):
        prompt = build_job_prompt(cv_text, job_text)
        answer = ask_llm(prompt)
        st.write(answer)

# -------------------
# MODE 3
# -------------------
elif mode == "CV Optimieren":
    job_text = st.text_area("Stellenanzeige einfügen")

    if st.button("CV optimieren"):
        prompt = build_cv_prompt(cv_text, job_text)
        answer = ask_llm(prompt)
        st.write(answer)