# Multi-stage Dockerfile for Loan Default Prediction
# Stage 1: Base image with Python dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create code directory
WORKDIR /code

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create code directory
WORKDIR /code

# Copy Python packages from base stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./
COPY data/ ./data/

# Create logs directory
RUN mkdir -p /code/logs && chown -R appuser:appuser /code

# Create startup script
RUN echo '#!/bin/bash\n\
    if [ "$SERVICE" = "api" ]; then\n\
    exec uvicorn main:app --host 0.0.0.0 --port 8000\n\
    else\n\
    exec streamlit run streamlit_app.py --server.port=8503 --server.address=0.0.0.0\n\
    fi' > /code/start.sh && chmod +x /code/start.sh

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8503 8000

# Health check for Streamlit
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8503/_stcore/health || exit 1

# Default command for Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8503", "--server.address=0.0.0.0"]

# Stage 3: Development image (optional)
FROM production as development

# Install development dependencies
USER root
RUN pip install --no-cache-dir \
    pytest \
    black \
    flake8 \
    jupyter

USER appuser

# Development command with auto-reload
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8503", "--server.address=0.0.0.0", "--server.runOnSave=true"]

ENV PYTHONPATH=/code