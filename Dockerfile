FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY fastapi_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (excluding models directory)
COPY fastapi_app/app.py .
COPY fastapi_app/scripts ./scripts
COPY fastapi_app/templates ./templates

# Create cache directory for model downloads
RUN mkdir -p /app/.cache && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]