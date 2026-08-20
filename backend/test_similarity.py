import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_collection(
    name="github_code"
)


# Question
query = "What is a path parameter?"


# Create query embedding
query_embedding = model.encode([query])


# Search only inside path-params.md
results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=20,
    where={
        "source": {
            "$eq": "../data\\docs\\en\\docs\\tutorial\\path-params.md"
        }
    }
)


# Print results
for i, (doc, metadata, distance) in enumerate(
    zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )
):

    print("=" * 60)

    print(f"Rank: {i}")
    print(f"Chunk ID: {metadata['chunk_id']}")
    print(f"Distance: {distance}")

    print("\nContent:")
    print(doc[:500])

print("=" * 60)