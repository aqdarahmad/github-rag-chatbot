"""Show the closest chunks in ChromaDB for a question (no reranking, no Gemini).

Run from the project root:
    python scripts/similarity_check.py "What is a path parameter?"
"""

import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

query = " ".join(sys.argv[1:]) or "What is a path parameter?"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
collection = client.get_collection(name="github_code")

results = collection.query(
    query_embeddings=[model.encode(query, normalize_embeddings=True).tolist()],
    n_results=5,
)

for rank, (document, metadata, distance) in enumerate(
    zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
):

    print("=" * 60)
    print(f"Rank: {rank + 1} | Distance: {distance:.4f}")
    print(f"Source: {metadata['source']} | Chunk: {metadata['chunk_id']}")
    print()
    print(document[:500])

print("=" * 60)
