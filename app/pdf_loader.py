# app/pdf_loader.py

"""
This file is responsible for:
- Reading multiple PDF files
- Extracting text from each PDF
- Returning clean text for further processing (chunking & embeddings)
"""

from pypdf import PdfReader
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts text from a single PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        # Extract text from each page
        text += page.extract_text() + "\n"

    return text


def load_multiple_pdfs(folder_path: str) -> dict:
    """
    Reads ALL PDFs from a folder and extracts text.
    
    Returns:
    {
        "file1.pdf": "text...",
        "file2.pdf": "text..."
    }
    """
    pdf_texts = {}
    folder = Path(folder_path)

    for pdf_file in folder.glob("*.pdf"):
        pdf_texts[pdf_file.name] = extract_text_from_pdf(pdf_file)

    return pdf_texts
