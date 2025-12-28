from sentence_transformers import SentenceTransformer

class EmbeddingModel:   
    def __init__(self):
        # Lightweight, fast, CPU-friendly model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed_texts(self, text):
        """Convert texts to embeddings"""
        return self.model.encode(text, show_progress_bar=True)
    
    def embed_query(self, query):
        """Convert query to embedding"""
        return self.model.encode(query)


"""     
LLMs cannot search text directly. We need to:
Convert text → numbers, Convert question → numbers, later->Compare numbers to find semantic similarity. This file does step 1 & 2.
Sentence transformers-> sentence embeddings, semantic similarity, retrieval 
We used MiniLM because it balances semantic quality and speed.
It produces 384-dimensional vectors which are ideal for FAISS
class : This avoids reloading the model for every request
Model: Strong semantic understanding
Pools token embeddings into one vector
chunk_vector ≈ [0.21, -0.12, ...]
query_vector ≈ [0.23, -0.10, ...]
These vectors will be close in space.
FAISS then finds this chunk as top result."""