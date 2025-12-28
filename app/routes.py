from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from pathlib import Path
import shutil

from app.pdf_loader import load_pdf
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore
from app.qa_engine import QAEngine


router = APIRouter()

# Global variables
embedding_model = EmbeddingModel()
qa_engine = QAEngine()
vector_store = None
active_pdf = None

UPLOAD_DIR = Path("data/uploaded_pdfs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, active_pdf     # session_id -> FAISSVectorStore

    # Validate file type FIRST
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Clear old PDFs
    for old_file in UPLOAD_DIR.glob("*.pdf"):
        old_file.unlink()

    # Save new file, Now the PDF exists on disk.
    pdf_path = UPLOAD_DIR / file.filename
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Step 1: Extract raw text & chunk
    chunks = load_pdf(str(pdf_path))

    if not chunks:
        raise HTTPException(status_code=400, detail="No text extracted from PDF")

    # Step 3: Embeddings
    embeddings = embedding_model.embed_texts(chunks)

    # Step 4: Vector store: Vector → chunk mapping
    vector_store = VectorStore(embedding_dim=len(embeddings[0]))
    vector_store.add(embeddings, chunks)

    active_pdf = file.filename

    return {
        "message": "PDF uploaded successfully",
        "filename": active_pdf,
        "chunks": len(chunks)
    }

@router.post("/ask")
async def ask_question(payload: dict):
    global vector_store, active_pdf
    
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded")
    
    question = payload.get("question", "").strip()      #Check missing data
    
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    # Embed question: Now both: Question & PDF chunks are in the same vector space.
    query_embedding = embedding_model.embed_query(question)
    
    # Retrieve similar chunks (THIS IS CONTEXT)
    results = vector_store.search(query_embedding, top_k=3)
    
    if not results:
        return {
            "answer": "No relevant information found in the document.",
            "source": active_pdf
        }
    
    # Generate answer
    answer = qa_engine.generate_answer(question, results)
    
    return {
        "answer": answer,
        "source": active_pdf,
        "chunks_found": len(results)
    }
""" async  → non-blocking request handling
global → modify shared app-level variables
/upload → process PDF & build FAISS index
/ask → answer questions using RAG
 """