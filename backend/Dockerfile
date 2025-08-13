# Base Python image
FROM python:3.11-slim

# Install system dependencies for Calibre
RUN apt-get update && apt-get install -y \
    wget xz-utils libgl1 libegl1 libxcb1 \
    libx11-6 libxrender1 libxext6 libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Install Calibre
RUN wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sh /dev/stdin

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ /app

# Expose API port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
