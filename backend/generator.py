import os

from dotenv import load_dotenv
from google import genai


# ==========================================
# Load environment variables
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise Exception(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )


# ==========================================
# Gemini client
# ==========================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# Model
# ==========================================

#MODEL_NAME = "gemini-3.6-flash"
MODEL_NAME = "gemini-3.1-flash-lite"


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

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


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