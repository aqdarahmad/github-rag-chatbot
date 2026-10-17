"""Show the closest chunks in ChromaDB for a question (no Gemini needed).

Run from the project root:
    python scripts/similarity_check.py "What is a path parameter?"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.retriever import retrieve  # noqa: E402


query = " ".join(sys.argv[1:]) or "What is a path parameter?"

for rank, chunk in enumerate(retrieve(query, top_k=5)):

    print("=" * 60)
    print(f"Rank: {rank + 1} | Distance: {chunk['distance']:.4f}")
    print(f"Source: {chunk['metadata']['source']} | Chunk: {chunk['metadata']['chunk_id']}")
    print()
    print(chunk["document"][:500])

print("=" * 60)
