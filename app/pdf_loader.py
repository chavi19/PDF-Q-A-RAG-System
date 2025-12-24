import fitz  # PyMuPDF

def load_pdf(pdf_path):
    """Extract text from PDF and split into chunks"""
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        text += page.get_text()
    
    # Simple chunking
    chunk_size = 800
    overlap = 200
    chunks = []
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    
    return chunks