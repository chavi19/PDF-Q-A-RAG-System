# app/text_chunker.py

import re

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list:
    """
    Splits text into overlapping chunks with soft sentence boundaries.
    """
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]

        # 🔥 Try to split at paragraph or sentence boundary
        split_point = max(
            chunk.rfind("\n\n"),
            chunk.rfind(". "),
            chunk.rfind("? "),
            chunk.rfind("! ")
        )

        if split_point > 0 and end != text_length:
            end = start + split_point + 1
            chunk = text[start:end]

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        start = max(end - overlap, 0)

    return chunks
