FROM python:3.10.13-slim-bullseye

# Set env vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

# Install essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Healthcheck 
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:$PORT/_stcore/health || exit 1

# Use exec form with shell expansion
CMD exec sh -c "streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0 --server.headless=true"