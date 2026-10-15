import logging
import os
import threading
import time

from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .rag import ask


logger = logging.getLogger("rag-chatbot")


# ==========================================
# Settings (can be changed with env variables)
# ==========================================

# Maximum characters in one question
MAX_QUESTION_LENGTH = int(
    os.getenv("MAX_QUESTION_LENGTH", "500")
)

# Maximum questions per IP inside the time window
RATE_LIMIT_REQUESTS = int(
    os.getenv("RATE_LIMIT_REQUESTS", "10")
)

# Time window in seconds
RATE_LIMIT_WINDOW_SECONDS = int(
    os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60")
)

# Extra frontend origins allowed to call the API
# Example: ALLOWED_ORIGINS=https://my-site.vercel.app
DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

EXTRA_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

# Built frontend (created by the Docker build)
FRONTEND_DIST = (
    Path(__file__).resolve().parent.parent
    / "frontend"
    / "frontend"
    / "dist"
)

SERVE_FRONTEND = (
    FRONTEND_DIST / "index.html"
).exists()


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="GitHub RAG Chatbot",
    description="RAG chatbot for FastAPI documentation",
    version="1.0.0"
)


# ==========================================
# Enable CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=DEFAULT_ORIGINS + EXTRA_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# Simple rate limiter (in memory, per IP)
# Protects the Gemini quota on a public demo
# ==========================================

_request_log = defaultdict(deque)

_request_log_lock = threading.Lock()


def get_client_ip(request: Request):

    forwarded = request.headers.get(
        "x-forwarded-for"
    )

    if forwarded:

        return forwarded.split(",")[0].strip()

    if request.client:

        return request.client.host

    return "unknown"


def check_rate_limit(ip: str):

    now = time.monotonic()

    with _request_log_lock:

        # Remove old entries of every IP so the
        # dictionary does not grow forever
        for key in list(_request_log.keys()):

            timestamps = _request_log[key]

            while (
                timestamps
                and now - timestamps[0]
                > RATE_LIMIT_WINDOW_SECONDS
            ):

                timestamps.popleft()

            if not timestamps and key != ip:

                del _request_log[key]

        timestamps = _request_log[ip]

        if len(timestamps) >= RATE_LIMIT_REQUESTS:

            raise HTTPException(
                status_code=429,
                detail=(
                    "Too many questions. "
                    "Please wait a minute and try again."
                )
            )

        timestamps.append(now)


# ==========================================
# Request Model
# ==========================================

class QuestionRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=MAX_QUESTION_LENGTH
    )


# ==========================================
# Health Endpoint
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ==========================================
# Ask Endpoint
# ==========================================

@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    http_request: Request
):

    check_rate_limit(
        get_client_ip(http_request)
    )

    try:

        answer = ask(request.question)

    except Exception:

        logger.exception(
            "Failed to generate an answer"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Could not generate an answer. "
                "Please try again."
            )
        )

    return {
        "question": request.question,
        "answer": answer
    }


# ==========================================
# Frontend
# If the frontend was built (Docker), the
# backend serves it, so one link is enough.
# Otherwise "/" is a simple status message.
# ==========================================

if SERVE_FRONTEND:

    app.mount(
        "/assets",
        StaticFiles(
            directory=FRONTEND_DIST / "assets"
        ),
        name="assets"
    )

    @app.get(
        "/{full_path:path}",
        include_in_schema=False
    )
    def serve_frontend(full_path: str):

        dist_root = FRONTEND_DIST.resolve()

        candidate = (
            dist_root / full_path
        ).resolve()

        # Files in the dist root (favicon, icons...)
        if (
            full_path
            and candidate.is_file()
            and dist_root in candidate.parents
        ):

            return FileResponse(candidate)

        # Any other path belongs to React Router
        return FileResponse(
            dist_root / "index.html"
        )

else:

    @app.get("/")
    def root():

        return {
            "message": "GitHub RAG Chatbot is running"
        }
