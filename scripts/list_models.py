"""List the Gemini models available for your API key.

Run from the project root:
    python scripts/list_models.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("GEMINI_API_KEY was not found. Check your .env file.")

client = genai.Client(api_key=api_key)

for model in client.models.list():
    print(model.name)
