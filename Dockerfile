FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV DB_NAME=major \
    DB_USER=root \
    DB_PASSWORD=password \
    DB_HOST=db \
    DB_PORT=5432 \
    OLLAMA_API_BASE=http://ollama:11434

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Set the default command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]