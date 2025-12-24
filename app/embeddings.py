from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed_texts(self, texts):
        """Convert texts to embeddings"""
        return self.model.encode(texts, show_progress_bar=True)
    
    def embed_query(self, query):
        """Convert query to embedding"""
        return self.model.encode(query)