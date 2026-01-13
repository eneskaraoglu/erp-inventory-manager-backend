# Backend Dockerfile - FastAPI
# Java Equivalent: Like building a JAR file and running with java -jar

# Stage 1: Python base image
FROM python:3.11-slim

# Set working directory (like cd /app)
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files
# PYTHONUNBUFFERED: Print output directly (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install dependencies first (Docker layer caching)
# This layer is cached if requirements.txt doesn't change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create data directory for SQLite database
RUN mkdir -p /app/data

# Expose port (documentation - doesn't actually publish)
EXPOSE 8001

# Health check - Docker will check if container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=5 \
    CMD curl -f http://localhost:8001/api/health || exit 1

# Run the application
# host=0.0.0.0 makes it accessible from outside container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
