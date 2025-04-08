FROM python:3.11-slim

WORKDIR /app

ENV DB_NAME=major \
    DB_USER=root \
    DB_PASSWORD=password \
    DB_HOST=db \
    DB_PORT=5432 \
    OLLAMA_API_BASE=http://ollama:11434

# Copy and install dependencies first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
