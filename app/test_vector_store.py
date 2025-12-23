from pdf_loader import load_multiple_pdfs
from text_chunker import chunk_text
from embeddings import EmbeddingModel
from vector_store import FAISSVectorStore

pdfs = load_multiple_pdfs("data/uploaded_pdfs")
embedder = EmbeddingModel()

vector_store = FAISSVectorStore(embedding_dim=384)

for pdf_name, text in pdfs.items():
    chunks = chunk_text(text)
    embeddings = embedder.embed_texts(chunks)
    vector_store.add_embeddings(embeddings, chunks, pdf_name)

query = "What is BERT?"
query_embedding = embedder.embed_query(query)

results = vector_store.search(query_embedding)

print("\n🔍 Search Results:")
for r in results:
    print(f"\n📄 Source: {r['source']}")
    print(r['text'][:300])
