# ==========================================
# Stage 1: build the React frontend
# ==========================================
FROM node:22-alpine AS frontend-build

WORKDIR /build

COPY frontend/frontend/package.json frontend/frontend/package-lock.json ./
RUN npm ci

COPY frontend/frontend/ ./
RUN npm run build


# ==========================================
# Stage 2: Python backend + built frontend
# ==========================================
FROM python:3.11-slim

# Hugging Face Spaces runs the container as user 1000
RUN useradd -m -u 1000 user

WORKDIR /home/user/app

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/home/user/.cache/huggingface \
    TOKENIZERS_PARALLELISM=false \
    ANONYMIZED_TELEMETRY=False

# Install the CPU-only version of torch first (much smaller than the
# default one), then everything else from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        "$(grep -i '^torch==' requirements.txt)" \
    && pip install --no-cache-dir -r requirements.txt

USER user

# Download the models while building, so the app starts fast
RUN python -c "from sentence_transformers import SentenceTransformer, CrossEncoder; SentenceTransformer('all-MiniLM-L6-v2'); CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

COPY --chown=user backend ./backend
COPY --chown=user chroma_db ./chroma_db
COPY --chown=user --from=frontend-build /build/dist ./frontend/frontend/dist

EXPOSE 7860

# Loading the models takes a while, so give the app time to start
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '7860') + '/health', timeout=4)"

# GEMINI_API_KEY must be provided as an environment variable / secret
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
