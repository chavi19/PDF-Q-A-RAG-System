from pdf_loader import load_multiple_pdfs

pdfs = load_multiple_pdfs("data/uploaded_pdfs")

for name, text in pdfs.items():
    print(f"\n--- {name} ---")
    print(text[:500])
