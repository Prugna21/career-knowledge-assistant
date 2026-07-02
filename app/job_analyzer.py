def build_job_prompt(cv_context, job_text):
    return f"""
Du bist ein professioneller Karriere-Analyst.

Vergleiche Lebenslauf und Stellenanzeige sehr genau.

WICHTIG:
- Sei präzise und faktenbasiert
- Keine Erfindungen
- Nutze klare Struktur

GIB DIE ANTWORT GENAU IN DIESER STRUKTUR:

MATCH_SCORE: (0–100)

STRENGTHS:
- ...

GAPS:
- ...

RECOMMENDATION:
- Ja / Nein / Vielleicht
- kurze Begründung

IMPROVEMENTS:
- konkrete Schritte zur Verbesserung des Profils

LEBENSLAUF:
{cv_context}

STELLENANZEIGE:
{job_text}
"""