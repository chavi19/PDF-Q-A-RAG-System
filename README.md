# PDF Question Answering System with RAG

A Retrieval-Augmented Generation (RAG) based system that allows users to upload PDF documents and ask questions, receiving accurate answers extracted from the document content using semantic search and AI-powered text generation.

---

## 🎯 Features

- **PDF Upload & Processing**: Extract and chunk text from PDF documents using PyMuPDF
- **Semantic Search**: Find relevant content using FAISS vector similarity search (L2 distance)
- **AI-Powered Answers**: Generate contextual answers using Google Flan-T5-base language model
- **REST API**: FastAPI backend with automatic API documentation (Swagger UI)
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Docker Support**: Fully containerized with Docker Compose for one-command deployment
---

## 🏗️ Architecture
```
User Query → Embedding Model → FAISS Search → Retrieved Chunks → LLM → Answer
```

**RAG Pipeline Flow:**
1. PDF Upload → Text Extraction (PyMuPDF)
2. Text Chunking (800 chars with 200 overlap)
3. Embedding Generation (MiniLM-L6-v2)
4. Vector Storage (FAISS IndexFlatL2)
5. Query → Embed → Similarity Search → Top-K Chunks
6. Context + Question → Flan-T5 → Generated Answer

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **LLM** | Google Flan-T5-base (CPU-optimized) |
| **PDF Processing** | PyMuPDF (fitz) |
| **Containerization** | Docker, Docker Compose |
| **Language** | Python 3.10 |

---

## 📁 Project Structure
```
PDF-Q-A-RAG-SYSTEM/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes.py            # API endpoints (/upload, /ask)
│   ├── pdf_loader.py        # PDF text extraction & chunking
│   ├── embeddings.py        # Embedding generation (MiniLM)
│   ├── vector_store.py      # FAISS vector operations
│   └── qa_engine.py         # Answer generation (Flan-T5)
├── frontend/
│   └── app.py               # Streamlit UI
├── data/
│   └── uploaded_pdfs/       # Persistent PDF storage
├── docs/
│   └── RAG_Notes.txt        #Detailed Notes
├── Dockerfile               # Backend container definition
├── Dockerfile.frontend      # Frontend container definition
├── docker-compose.yml       # Multi-container orchestration
├── .dockerignore           # Files to exclude from Docker build
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📚 Learning Resources

**`docs/RAG_Notes.txt`**: Personal learning notes documenting my journey building this RAG system, including:
- Key concepts and architectural decisions
- Challenges faced and solutions implemented
- Resources and references used during development
- Best practices learned for production RAG systems

Feel free to check out my notes to understand the thought process behind implementation decisions!

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.10+
- Docker & Docker Desktop (for containerized deployment)
- Git

---

### **Option 1: Docker Deployment (Recommended)**

**Quick Start - One Command:**
```bash
# Clone the repository
git clone https://github.com/chavi19/PDF-Q-A-RAG-SYSTEM.git
cd PDF-Q-A-RAG-SYSTEM

# Build and run with Docker Compose
docker-compose up --build
```

**Access:**
- **Frontend UI**: http://localhost:8501
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

**Stop Containers:**
```bash
# Stop (Ctrl+C in terminal, or)
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

### **Option 2: Local Development Setup**

1. **Clone the repository**
```bash
git clone https://github.com/chavi19/PDF-Q-A-RAG-SYSTEM.git
cd PDF-Q-A-RAG-SYSTEM
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend** (Terminal 1)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Run the frontend** (Terminal 2)
```bash
streamlit run frontend/app.py
```

6. **Access the application**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

---

## 🔧 How It Works

### **1. Document Processing**
- PDF uploaded via Streamlit UI
- Text extracted using PyMuPDF (handles complex layouts)
- Text cleaned and normalized

### **2. Smart Chunking**
- Text split into overlapping chunks (800 characters)
- 200-character overlap preserves context
- Attempts sentence-boundary splitting for coherence

### **3. Embedding Generation**
- Each chunk converted to 384-dimensional vector
- Uses `all-MiniLM-L6-v2` (fast, efficient, accurate)
- Same model for documents and queries ensures semantic matching

### **4. Vector Indexing**
- Embeddings stored in FAISS `IndexFlatL2`
- L2 (Euclidean) distance for similarity measurement
- Efficient search across thousands of chunks

### **5. Query Processing**
- User question embedded with same model
- Top-3 most similar chunks retrieved
- Ranked by distance (lower = more similar)

### **6. Answer Generation**
- Retrieved chunks + question sent to Flan-T5
- Model generates natural language answer
- Response limited to document context only

---

## 📊 API Endpoints

### **Health Check**
```http
GET /
```
**Response:**
```json
{
  "message": "PDF Q&A System is running"
}
```

---

### **Upload PDF**
```http
POST /upload
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "message": "PDF uploaded successfully",
  "filename": "document.pdf",
  "chunks": 45
}
```

---

### **Ask Question**
```http
POST /ask
Content-Type: application/json

{
  "question": "What is the refund policy?"
}
```

**Response:**
```json
{
  "answer": "The refund policy allows returns within 30 days of purchase with proof of receipt.",
  "source": "document.pdf",
  "chunks_found": 3
}
```

---

## 🐳 Docker Architecture

### **Multi-Container Setup:**
```yaml
services:
  backend:
    - FastAPI app on port 8000
    - Processes PDFs and handles AI inference
    
  frontend:
    - Streamlit UI on port 8501
    - Communicates with backend via Docker network
```

### **Key Docker Features:**
- **Layer Caching**: Requirements installed separately for fast rebuilds
- **Volume Mounting**: Uploaded PDFs persist across restarts
- **CORS Middleware**: Enables frontend-backend communication
- **Health Checks**: Automatic container health monitoring
- **CPU-Only PyTorch**: Optimized for size and speed (no GPU needed)

---

## 📦 Dependencies
```txt
fastapi              # Web framework
uvicorn             # ASGI server
streamlit           # Frontend UI
python-multipart    # File upload handling
PyMuPDF             # PDF text extraction
sentence-transformers  # Embedding model
faiss-cpu           # Vector search
transformers        # LLM interface
torch (CPU-only)    # PyTorch backend
numpy               # Numerical operations
requests            # HTTP client
```

---

## 🎓 What I Learned

- **RAG Implementation**: Building end-to-end retrieval-augmented generation pipelines
- **Vector Databases**: Semantic search with FAISS for efficient similarity matching
- **Transformer Models**: Using sentence-transformers and Flan-T5 for NLP tasks
- **API Development**: Creating REST APIs with FastAPI and automatic documentation
- **Containerization**: Docker multi-container orchestration with Docker Compose
- **Production Deployment**: Best practices for deploying ML models
- **Frontend-Backend Integration**: CORS, environment variables, and service communication

---

## 🔮 Future Improvements

- [ ] **Multi-Document Support**: Query across multiple PDFs simultaneously
- [ ] **Conversation Memory**: Context-aware follow-up questions
- [ ] **Better LLM Integration**: Support for GPT-4o-mini or Claude API
- [ ] **Citation Tracking**: Show exact source text with page numbers
- [ ] **Hybrid Search**: Combine keyword and semantic search
- [ ] **Response Caching**: Redis for repeated questions
- [ ] **User Authentication**: JWT-based multi-user support
- [ ] **Evaluation Metrics**: Track answer accuracy and relevance
- [ ] **Cloud Deployment**: Kubernetes setup for production scaling
- [ ] **Advanced Chunking**: Semantic chunking based on document structure

---


## ⭐ Star this repository if you found it helpful!

**Built with ❤️ using RAG, FastAPI, Streamlit, and Docker**
