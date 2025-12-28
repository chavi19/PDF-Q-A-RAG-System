import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_dim):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []
    
    #storing document knowledge
    def add(self, embeddings, chunks):
        """Add embeddings to FAISS index"""
        vectors = np.array(embeddings).astype("float32")    #Convert embeddings => FAISS only accepts float32
        faiss.normalize_L2(vectors)
        self.index.add(vectors)     #FAISS now stores vectors internally like: [ v0, v1, v2, v3, ... ]
        self.chunks = chunks        #Mapping:  FAISS index:0  maps to	chunks[0]
    
    def search(self, query_embedding, top_k=3):
        """Search for similar chunks"""
        query_vector = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector, top_k)     #Smaller distance = better match
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx >= 0 and idx < len(self.chunks):
                results.append({
                    "text": self.chunks[idx],
                    "distance": float(dist)
                })
        
        return results
"""
FAISS does NOT understand text, FAISS only understands vectors, Extremely fast similarity search
class:(FAISS index =>Fast similarity search & self.chunk => Map vector → original text) Store document embeddings & retrieve most semantically similar text chunks for a query. This is the Retrieval part of RAG.
FAISS requires NumPy arrays (float32), SentenceTransformer outputs NumPy-compatible vectors 
embedding_dim= Size of each vector- For all-MiniLM-L6-v2 → 384
Flat → exact search (no approximation) & L2(cosine similarity) → Euclidean distance
What is IndexFlatL2?
"Flat" = exhaustive search (checks all vectors)
"L2" = Euclidean distance metric
Distance score meaning: Lower = more similar, 0.0 = identical, 2.0 = very different
Each (idx, dist) pair corresponds to: A document chunk & Its similarity score"""