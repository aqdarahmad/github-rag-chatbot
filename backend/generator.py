import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==========================================
# Environment variables
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Local development: read the .env file from the project root.
# In deployment the variables come from the host (secrets / env vars).
load_dotenv(BASE_DIR / ".env")


# ==========================================
# Model
# ==========================================

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


class MissingAPIKeyError(RuntimeError):
    """Raised when GEMINI_API_KEY is not configured."""


# ==========================================
# Gemini client (created on first use, so the
# app can still start and answer /health even
# if the key is missing)
# ==========================================

@lru_cache(maxsize=1)
def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise MissingAPIKeyError(
            "GEMINI_API_KEY was not found. "
            "Add it to your .env file (local) or to the "
            "secrets / environment variables of your host."
        )

    return genai.Client(api_key=api_key)


# ==========================================
# Generate answer
# ==========================================

def generate_answer(question, context):

    prompt = f"""
You are a helpful assistant specialized in FastAPI.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
say that you don't have enough information.

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # response.text can be empty when the answer is blocked
    return response.text or (
        "I could not generate an answer for this question."
    )


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about FastAPI: "
    )

    context = """
FastAPI allows you to declare path parameters
using curly braces in the URL.

Example:

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

The value of item_id is extracted from the URL
and converted to an integer.
"""

    answer = generate_answer(
        question,
        context
    )

    print("\n==============================")
    print("Generated Answer")
    print("==============================\n")

    print(answer)
