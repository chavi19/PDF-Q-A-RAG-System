from pdf_loader import load_multiple_pdfs
from text_chunker import chunk_text
from embeddings import EmbeddingModel

pdfs = load_multiple_pdfs("data/uploaded_pdfs")

embedder = EmbeddingModel()

for file, text in pdfs.items():
    chunks = chunk_text(text)
    vectors = embedder.embed_texts(chunks)

    print(f"\n📄 {file}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embedding shape: {len(vectors)} x {len(vectors[0])}")
