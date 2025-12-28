from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="PDF Q&A RAG System")
# Include all API routes
app.include_router(router)

@app.get("/")
def root():
    #to verify backend is running.
    return {"message": "PDF Q&A System is running"}

""" 
Starts the FastAPI server
Registers routes """