from pathlib import Path
from pdf_reader import read_pdf
from text_splitter import split_text
from search import simple_search
from ai_engine import ask_llm
from job_analyzer import build_job_prompt
from cv_optimizer import build_cv_prompt

cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

cv_text = read_pdf(pdf_files[0])
chunks = split_text(cv_text)

print("\nCareer Assistant")
print("1 = Frage zum Lebenslauf")
print("2 = Stellenanalyse")
print("3 = CV für Job optimieren")

mode = input("\nWähle Modus (1/2/3): ")

if mode == "1":
    question = input("\nFrage:\n> ")

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
    print("\nAntwort:\n")
    print(answer)

elif mode == "2":
    print("\nStellenanzeige einfügen (CTRL+D / CTRL+Z):\n")
    import sys
    job_text = sys.stdin.read()

    prompt = build_job_prompt(cv_text, job_text)

    answer = ask_llm(prompt)

    print("\nJob Analyse:\n")
    print(answer)

elif mode == "3":
    print("\nStellenanzeige einfügen (CTRL+D / CTRL+Z):\n")
    import sys
    job_text = sys.stdin.read()

    prompt = build_cv_prompt(cv_text, job_text)

    answer = ask_llm(prompt)

    print("\nOptimierter CV:\n")
    print(answer)