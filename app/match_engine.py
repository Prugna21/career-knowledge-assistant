import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_match_score(cv_text, job_text):
    """
    Returns:
        score (0-100),
        explanation string
    """

    embeddings = model.encode([cv_text, job_text])

    cv_emb = embeddings[0]
    job_emb = embeddings[1]

    # cosine similarity
    similarity = np.dot(cv_emb, job_emb) / (
        np.linalg.norm(cv_emb) * np.linalg.norm(job_emb)
    )

    score = float(similarity * 100)
    score = max(0, min(100, score))

    explanation = generate_explanation(score)

    return round(score, 1), explanation


def generate_explanation(score):
    if score > 80:
        return "Sehr guter Fit zwischen CV und Job."
    elif score > 60:
        return "Solider Match, einige Skills passen gut."
    elif score > 40:
        return "Teilweiser Match, mehrere Lücken vorhanden."
    else:
        return "Schwacher Match, CV passt nur begrenzt zum Job."