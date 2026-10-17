"""Print the chunks stored in ChromaDB for one source file.

Run from the project root:
    python scripts/inspect_chunks.py path-params.md
"""

import sys
from pathlib import Path

import chromadb


BASE_DIR = Path(__file__).resolve().parent.parent

if len(sys.argv) < 2:
    raise SystemExit("Usage: python scripts/inspect_chunks.py <part of the file path>")

needle = sys.argv[1]

client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
collection = client.get_collection(name="github_code")

data = collection.get(include=["documents", "metadatas"])

found = 0

for document, metadata in zip(data["documents"], data["metadatas"]):

    if needle in metadata["source"]:

        found += 1

        print(f"[{metadata['source']} | chunk {metadata['chunk_id']}]")
        print(document[:200])
        print("---")

print(f"\n{found} chunk(s) matched '{needle}'.")
