# PDF Question Answering System with RAG

A Retrieval-Augmented Generation (RAG) based system that allows users to upload PDF documents and ask questions, receiving accurate answers extracted from the document content.

## 🎯 Features

- **PDF Upload & Processing**: Extract and chunk text from PDF documents
- **Semantic Search**: Find relevant content using FAISS vector similarity search
- **AI-Powered Answers**: Generate contextual answers using Flan-T5 language model
- **REST API**: FastAPI backend for scalable deployment
- **Interactive UI**: Clean Streamlit interface for easy interaction

## 🏗️ Architecture
```
User Query → Embedding Model → FAISS Search → Retrieved Chunks → LLM → Answer
```

**Tech Stack:**
- **Backend**: FastAPI, Python
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **LLM**: Flan-T5-base (Text-to-Text Generation)
- **PDF Processing**: PyMuPDF
- **Frontend**: Streamlit

## 📁 Project Structure
```
PDF-Q-A-RAG-SYSTEM/
├── app/
│   ├── main.py              # FastAPI application
│   ├── routes.py            # API endpoints
│   ├── pdf_loader.py        # PDF text extraction
│   ├── embeddings.py        # Embedding generation
│   ├── vector_store.py      # FAISS vector operations
│   └── qa_engine.py         # Answer generation
├── frontend/
│   └── app.py               # Streamlit UI
├── data/
│   └── uploaded_pdfs/       # Temporary PDF storage
├── requirements.txt
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/PDF-Q-A-RAG-SYSTEM.git
cd PDF-Q-A-RAG-SYSTEM
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the backend**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Run the frontend** (in a new terminal)
```bash
streamlit run frontend/app.py
```

5. **Access the application**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 📦 Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

## 🔧 How It Works

1. **Document Processing**: PDF is uploaded and text is extracted using PyMuPDF
2. **Chunking**: Text is split into overlapping chunks (800 chars, 200 overlap)
3. **Embedding**: Each chunk is converted to a 384-dimensional vector using MiniLM
4. **Indexing**: Vectors are stored in FAISS for fast similarity search
5. **Query Processing**: User question is embedded and similar chunks are retrieved
6. **Answer Generation**: Retrieved context + question is sent to Flan-T5 for answer generation

## 📊 API Endpoints

### `POST /upload`
Upload a PDF document
```json
{
  "file": "document.pdf"
}

### `POST /ask`
Ask a question
```json
{
  "question": "What is the refund policy?"
}

🎓 What I Learned

- Implementing RAG (Retrieval-Augmented Generation) pipelines
- Vector similarity search with FAISS
- Semantic embeddings with transformer models
- Building REST APIs with FastAPI
- Deploying ML models in production
- Managing vector databases

🔮 Future Improvements

- [ ] Support for multiple PDF uploads simultaneously
- [ ] Add conversation memory for follow-up questions
- [ ] Integrate better LLMs (GPT-4)
- [ ] Add citation tracking for answers
- [ ] Implement caching for faster responses
- [ ] Add authentication and user sessions


👤 Author

Chavi Maru
GitHub: https://github.com/chavi19
LinkedIn: https://linkedin.com/in/yourprofile

---

⭐ Star this repo if you found it helpful!
