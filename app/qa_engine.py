#brain- LLM
'''The QA engine takes the user’s question, retrieves the most relevant chunks using FAISS, and feeds them to an LLM to generate a grounded answer
This file:
- Takes a user question
- Retrieves relevant chunks from FAISS
- Sends context + question to LLM
'''

from transformers import pipeline

class QAEngine:
    def __init__(self):
        self.model = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            max_new_tokens=150,
            device=-1
        )
    
    def generate_answer(self, question, chunks):
        """Generate answer from retrieved chunks"""
        # Build context
        chunks = sorted(chunks, key=lambda x: x["distance"])[:4]

        context = "\n\n".join([c["text"][:500] for c in chunks])    #LLMs have token limits
        #Take all retrieved chunks, extract only the first 500 characters of each, and combine them into one context string, send to LLM.
        #Generates answer using retrieved chunks as context.
        #prompt = context(rel chunks) + query + the instructions return below, all together passed
        prompt = f"""
You are an AI assistant answering questions from a document. 
Use the information provided below to answer the question. 
Base your answer strictly on the document content. 
If multiple answers are present, choose the most relevant one. 
If the answer is not clearly present, say so briefly. 

INSTRUCTIONS: 
If the question asks to LIST items, list only names. 
If the question asks about a SECTION, summarize only that section. 
If the question is factual, answer in one concise sentence. 
If multiple choices are present, select the exact correct option as written. 
If the document contains tables, extract only the relevant column values. 
If the question asks for personal or resume details, extract them exactly. 
If steps or procedures are asked, list them in order as in the document. 
If dates or timelines are asked, include only the relevant dates.
Document Excerpts:
{context}

Question:
{question}

Answer:
"""

        
        # Generate
        try:
            result = self.model(prompt, max_length=200)
            answer = result[0]["generated_text"].strip()
            
            if len(answer) < 10:
                return "Cannot generate a clear answer from the document."
            
            return answer
        except Exception as e:
            return f"Error: {str(e)}"
#prompt → model → list → dict → generated_text → clean answer
        
#uvicorn app.main:app --reload --host 0.0.0.0 --port 8000