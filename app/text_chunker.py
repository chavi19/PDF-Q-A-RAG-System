# app/text_chunker.py

"""
This file:
- Takes extracted PDF text
- Splits it into overlapping chunks
- Prepares data for embeddings
"""

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list:
    """
    Splits text into overlapping chunks.

    Args:
        text (str): Full document text
        chunk_size (int): Characters per chunk
        overlap (int): Overlapping characters

    Returns:
        List of text chunks
    """
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward with overlap
        start = end - overlap

    return chunks
