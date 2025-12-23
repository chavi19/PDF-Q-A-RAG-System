# app/vector_store.py

"""
This file:
- Creates a FAISS index
- Stores embeddings
- Performs similarity search
"""

import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, embedding_dim: int):
        # L2 distance index (works well with MiniLM)
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.text_chunks = []   # stores actual chunk text
        self.metadata = []      # stores PDF name etc.

    def add_embeddings(self, embeddings, chunks, pdf_name):
        """
        Adds embeddings + metadata to FAISS index.
        """
        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)

        for chunk in chunks:
            self.text_chunks.append(chunk)
            self.metadata.append(pdf_name)

    def search(self, query_embedding, top_k=5):
        """
        Searches FAISS index and returns top-k results.
        """
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            results.append({
                "text": self.text_chunks[idx],
                "source": self.metadata[idx]
            })

        return results
