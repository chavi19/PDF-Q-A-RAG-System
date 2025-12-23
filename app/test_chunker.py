from pdf_loader import load_multiple_pdfs
from text_chunker import chunk_text

pdfs = load_multiple_pdfs("data/uploaded_pdfs")

for file_name, text in pdfs.items():
    chunks = chunk_text(text)
    print(f"\n📄 {file_name}")
    print(f"Total chunks: {len(chunks)}")
    print("Sample chunk:\n", chunks[0][:300])
