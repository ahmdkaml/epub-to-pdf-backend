FROM python:3.11-slim

WORKDIR /app

# Install only what’s needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 libxslt1.1 libffi8 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
