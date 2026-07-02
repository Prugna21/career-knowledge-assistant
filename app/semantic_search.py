from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2") # https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2


def build_index(chunks):
    return model.encode(chunks)


def search(query, chunks, chunk_embeddings, top_k=4):
    query_embedding = model.encode([query])[0]

    scores = np.dot(chunk_embeddings, query_embedding)

    top_indices = np.argsort(scores)[::-1][:top_k]

    return [chunks[i] for i in top_indices]