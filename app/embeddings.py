# app/embeddings.py

"""
This file:
- Loads a sentence-transformer model
- Converts text chunks into embeddings
"""

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self):
        # Lightweight, fast, CPU-friendly model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_texts(self, texts: list) -> list:
        """
        Converts list of text chunks into embeddings.
        """
        return self.model.encode(texts, show_progress_bar=True)

    def embed_query(self, query: str):
        """
        Converts user question into embedding.
        """
        return self.model.encode(query)
