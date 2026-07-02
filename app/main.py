from pathlib import Path
from pdf_reader import read_pdf
from text_splitter import split_text
from semantic_search import build_index, search
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from cv_optimizer import build_cv_prompt
import sys

# -------------------
# CV laden
# -------------------
cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

if not pdf_files:
    print("Kein CV gefunden")
    exit()

cv_text = read_pdf(pdf_files[0])
chunks = split_text(cv_text)


# -------------------
# MENU
# -------------------
print("\nCareer Assistant")
print("1 = Frage zum Lebenslauf")
print("2 = Stellenanalyse")
print("3 = CV für Job optimieren")

mode = input("\nWähle Modus (1/2/3): ")


# -------------------
# MODE 1
# -------------------
if mode == "1":
    question = input("\nFrage:\n> ")

    relevant_chunks = semantic_search(question, chunks, embeddings)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
Du bist ein präziser Karriere-Experte.

KONTEXT:
{context}

FRAGE:
{question}
"""

    print("\nAntwort:\n")
    print(ask_llm(prompt))


# -------------------
# MODE 2
# -------------------
elif mode == "2":
    print("\nStellenanzeige einfügen (CTRL+D / CTRL+Z):\n")
    job_text = sys.stdin.read()

    prompt = build_job_prompt(cv_text, job_text)

    print("\nJob Analyse:\n")
    print(ask_llm(prompt))


# -------------------
# MODE 3
# -------------------
elif mode == "3":
    print("\nStellenanzeige einfügen (CTRL+D / CTRL+Z):\n")
    job_text = sys.stdin.read()

    prompt = build_cv_prompt(cv_text, job_text)

    print("\nOptimierter CV:\n")
    print(ask_llm(prompt))