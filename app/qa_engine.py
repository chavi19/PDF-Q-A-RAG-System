# app/qa_engine.py

"""
This file:
- Takes a user question
- Retrieves relevant chunks from FAISS
- Sends context + question to LLM
"""

from transformers import pipeline


class QAEngine:
    def __init__(self):
        # Lightweight open-source model (no API key needed)
        self.qa_pipeline = pipeline(
            "text2text-generation",
            model="declare-lab/flan-alpaca-base",
            max_new_tokens=256
        )

    def generate_answer(self, question, retrieved_chunks):
        """
        Generates answer using retrieved chunks as context.
        """
        retrieved_chunks = retrieved_chunks[:3]

        context = "\n\n".join(
            [chunk["text"][:500] for chunk in retrieved_chunks]
        )

        prompt = f"""
You are a policy document assistant.

Answer the question strictly using the provided context.
If the answer is not present in the context, say:
"Answer not available in the document.

Context:
{context}

Question:
{question}

Answer clearly and concisely.
"""

        response = self.qa_pipeline(prompt)
        return response[0]["generated_text"]
