def build_cv_prompt(cv_text, job_text):
    return f"""
Du bist ein professioneller CV-Optimierer.

Deine Aufgabe ist es, den Lebenslauf so umzuschreiben, dass er perfekt zur Stellenanzeige passt.

REGELN:
- Erfinde nichts
- Nutze nur vorhandene Informationen aus dem CV
- Priorisiere relevante Erfahrungen
- Mache den CV klar, strukturiert und ATS-freundlich

GIB DEN OPTIMIERTEN CV IN DIESEM FORMAT:

1. PROFILZUSAMMENFASSUNG
2. RELEVANTE ERFAHRUNG
3. SKILLS
4. AUSGEWÄHLTE PROJEKTE (falls vorhanden)
5. AUSBILDUNG
6. OPTIONAL: EMPFOHLENE ERGÄNZUNGEN

LEBENSLAUF:
{cv_text}

STELLENANZEIGE:
{job_text}
"""