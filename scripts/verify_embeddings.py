"""Check that the ONNX embeddings match the vectors already stored in chroma_db/.

The database was originally built with sentence-transformers. The app now
embeds questions with the ONNX version of the same model, so the stored vectors
and the new ones must agree. Run this once:

    python scripts/verify_embeddings.py

Expected: "OK" with similarity ~1.0. If it prints "MISMATCH", rebuild the
database with:  python -m backend.embeddings
"""

import random
import sys
from pathlib import Path

import chromadb
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.embedder import embed  # noqa: E402


BASE_DIR = Path(__file__).resolve().parent.parent

collection = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db")).get_collection("github_code")

data = collection.get(include=["documents", "embeddings"])

total = len(data["ids"])

sample = random.Random(0).sample(range(total), min(30, total))

similarities = []

for index in sample:

    stored = np.array(data["embeddings"][index], dtype=np.float32)
    stored /= np.linalg.norm(stored)

    new = np.array(embed([data["documents"][index]])[0], dtype=np.float32)

    similarities.append(float(np.dot(stored, new)))

print(f"Checked {len(sample)} of {total} chunks")
print(f"Cosine similarity  min: {min(similarities):.4f}  average: {np.mean(similarities):.4f}")

if min(similarities) > 0.99:
    print("OK: the stored vectors match the ONNX embeddings.")
else:
    print("MISMATCH: rebuild the database with:  python -m backend.embeddings")
