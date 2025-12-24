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
        context = "\n\n".join([c["text"][:500] for c in chunks])
        
        # Create prompt
        prompt = f"""Answer the question based on the context.

Context:
{context}

Question: {question}

Answer:"""
        
        # Generate
        try:
            result = self.model(prompt, max_length=200)
            answer = result[0]["generated_text"].strip()
            
            if len(answer) < 10:
                return "Cannot generate a clear answer from the document."
            
            return answer
        except Exception as e:
            return f"Error: {str(e)}"