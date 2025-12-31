from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(title="PDF Q&A RAG System")
#ADD CORS (necessary for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (fine for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include all API routes
app.include_router(router)

@app.get("/")
def root():
    #to verify backend is running.
    return {"message": "PDF Q&A System is running"}

""" 
Starts the FastAPI server
Registers routes """