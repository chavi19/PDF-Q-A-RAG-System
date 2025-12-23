from pdf_loader import load_multiple_pdfs
from text_chunker import chunk_text
from embeddings import EmbeddingModel
from vector_store import FAISSVectorStore
from qa_engine import QAEngine

# Load PDFs
pdfs = load_multiple_pdfs("data/uploaded_pdfs")

embedder = EmbeddingModel()
vector_store = FAISSVectorStore(embedding_dim=384)
qa_engine = QAEngine()

# Index PDFs
for pdf_name, text in pdfs.items():
    chunks = chunk_text(text)
    embeddings = embedder.embed_texts(chunks)
    vector_store.add_embeddings(embeddings, chunks, pdf_name)

# Ask question
question = "What is BERT?"
query_embedding = embedder.embed_query(question)

retrieved_chunks = vector_store.search(query_embedding)
answer = qa_engine.generate_answer(question, retrieved_chunks)

print("\n🤖 Answer:\n")
print(answer)
