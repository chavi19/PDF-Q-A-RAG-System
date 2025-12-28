import fitz  # PyMuPDF

MAX_CHUNKS = 2000  # hard safety cap- Prevents RAM crash (MemoryError)

def load_pdf(pdf_path):
    doc = fitz.open(pdf_path)   #Opens PDF as a list of pages
    text = []

    for page in doc:        #Extracting text page-by-page
        page_text = page.get_text()
        if page_text:
            text.append(page_text)

    doc.close()         #avoids memory leaks

    full_text = "\n".join(text).strip()     #Combining all pages into one clean string
    if not full_text:   #PDF had images only safely return an empty list instead of crashing
        return []

    chunk_size = 800
    overlap = 200       #So we don’t lose meaning at chunk boundaries.
    chunks = []

    start = 0
    text_length = len(full_text)    #total characters

    while start < text_length and len(chunks) < MAX_CHUNKS:     #Sliding window chunking loop
        end = min(start + chunk_size, text_length)

        # Prevents: Infinite loops, CPU freeze
        if end <= start:
            break

        chunk = full_text[start:end].strip()
        if len(chunk) > 50:     #Removing garbage chunks
            chunks.append(chunk)

        # No text loss between chunks, No negative indexing
        start = end - overlap
        if start < 0:   
            start = 0

        # reached the end of document
        if end == text_length:
            break

    return chunks

""" fitz is the Python import name for PyMuPDF, Used only to open PDFs and extract text
pdf_path: Take a PDF file → return all text inside it as a single string. No chunking. No embeddings. Only extraction. 
doc = [page1, page2, page3, ...] Each page → extract text, Store page by page in a list
.strip()=>"\n\nHello World\n\n" → "Hello World"==Clean input for chunking, Avoids empty chunks later 
Open PDF-> Loop through pages-> Extract text from each page-> Combine all text-> Return a single clean string"""