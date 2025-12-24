from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="PDF Q&A RAG System")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "PDF Q&A System is running"}