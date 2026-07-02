from pathlib import Path
from pdf_reader import read_pdf
from ai_engine import ask_llm

cv_folder = Path("data/cv")
pdf_files = list(cv_folder.glob("*.pdf"))

cv_text = read_pdf(pdf_files[0])

question = input("\nFrage zu deinem Lebenslauf:\n> ")

prompt = f"""
Du bist ein Karriere-Assistent.

Nutze nur den Lebenslauf unten, um die Frage zu beantworten.

LEBENSLAUF:
{cv_text}

FRAGE:
{question}
"""

answer = ask_llm(prompt)

print("\nAntwort:\n")
print(answer)