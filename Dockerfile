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
# (no PyTorch, small enough for free hosting)
# ==========================================
FROM python:3.11-slim

# Run as a normal user (Hugging Face Spaces requires user 1000)
RUN useradd -m -u 1000 user \
    && mkdir -p /home/user/app \
    && chown user:user /home/user/app

WORKDIR /home/user/app

ENV PYTHONUNBUFFERED=1 \
    ANONYMIZED_TELEMETRY=False

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER user

COPY --chown=user backend ./backend
COPY --chown=user data ./data

# Build the vector database while building the image. This also downloads the
# small ONNX embedding model, so the app starts fast and the database always
# matches the model used to embed the questions.
RUN python -m backend.embeddings

COPY --chown=user --from=frontend-build /build/dist ./frontend/frontend/dist

EXPOSE 7860

# Loading the model takes a little while, so give the app time to start
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '7860') + '/health', timeout=4)"

# GEMINI_API_KEY must be provided as an environment variable / secret
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
