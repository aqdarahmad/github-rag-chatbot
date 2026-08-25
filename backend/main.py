from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .rag import ask


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

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# Request Model
# ==========================================

class QuestionRequest(BaseModel):

    question: str


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/")
def root():

    return {
        "message": "GitHub RAG Chatbot is running"
    }


# ==========================================
# Ask Endpoint
# ==========================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = ask(request.question)

    return {
        "question": request.question,
        "answer": answer
    }