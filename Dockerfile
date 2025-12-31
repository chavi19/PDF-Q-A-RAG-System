FROM python:3.10-slim

WORKDIR /app

# Debug: Show what files exist
RUN echo "=== Current directory ===" && pwd
RUN echo "=== Files in build context ===" && ls -la / || true

# Try to copy
COPY requirements.txt .

# Verify it copied
RUN echo "=== Files in /app ===" && ls -la

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]