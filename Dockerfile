# Dockerfile in your main cert-coordination-observability directory
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files
COPY cert/ ./cert/
COPY examples/ ./examples/
COPY integrations/ ./integrations/
COPY ll_providers/ ./ll_providers/
COPY setup.py .
COPY .env .

# Install the package
RUN pip install -e .

EXPOSE 8000
CMD ["python", "-m", "cert.api.server"]