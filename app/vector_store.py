import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_dim):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []
    
    def add(self, embeddings, chunks):
        """Add embeddings to FAISS index"""
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.chunks = chunks
    
    def search(self, query_embedding, top_k=3):
        """Search for similar chunks"""
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0 and idx < len(self.chunks):
                results.append({
                    "text": self.chunks[idx],
                    "distance": float(dist)
                })
        
        return results