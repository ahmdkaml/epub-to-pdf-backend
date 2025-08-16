FROM python:3.11-slim

WORKDIR /app

# Install only runtime libs (only if your deps really need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 libxslt1.1 libffi8 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/ .

# Expose is optional on Railway, but doesn’t hurt
EXPOSE 8000

# Run uvicorn on the port Railway sets
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

