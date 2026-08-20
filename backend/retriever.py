import chromadb
from sentence_transformers import SentenceTransformer


# ==========================================
# Embedding model
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ==========================================
# Connect to ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path="../chroma_db"
)

collection = client.get_collection(
    name="github_code"
)


# ==========================================
# Search ChromaDB
# ==========================================

def search(query, top_k=20):

    # Convert user's question to embedding
    query_embedding = model.encode(
        [query]
    )

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    for i, doc in enumerate(results['documents'][0]):
        print(f"[{i}] {doc[:150]}")
        print("---")

    return results


# ==========================================
# Select relevant chunks
# ==========================================

def select_relevant_chunks(results, query, max_chunks=5):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []

    query_lower = query.lower()

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        text = document.lower()

        # Start with semantic distance
        score = distance

        # ==========================================
        # Keyword matching
        # ==========================================

        if "path parameter" in query_lower:
            if "path parameter" in text:
                score -= 0.30

        # ==========================================
        # Strong boost for definition
        # ==========================================

        if "path parameters" in text:

            if "you can declare path" in text:
                score -= 0.50

            if "value of the path parameter" in text:
                score -= 0.10

        # ==========================================
        # Penalize specialized topics
        # ==========================================

        if "path parameters containing paths" in text:
            score += 0.20

        if "predefined values" in text:
            score += 0.15

        if "enumeration" in text:
            score += 0.10

        chunks.append({
            "document": document,
            "metadata": metadata,
            "distance": distance,
            "score": score
        })

    # Lower score = better
    chunks.sort(
        key=lambda x: x["score"]
    )

    return chunks[:max_chunks]


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    query = input(
        "\nAsk a question about FastAPI: "
    )


    # ======================================
    # Retrieve 20 chunks from ChromaDB
    # ======================================

    results = search(query)


    # ======================================
    # Select best 5 chunks
    # ======================================

    selected_chunks = select_relevant_chunks(
        results,
        query,
        max_chunks=5
    )


    # ======================================
    # Display results
    # ======================================

    print("\n==============================")
    print("Selected relevant chunks")
    print("==============================\n")


    for i, chunk in enumerate(
        selected_chunks
    ):

        print(
            f"Result {i + 1}"
        )

        print(
            f"Source: "
            f"{chunk['metadata']['source']}"
        )

        print(
            f"Chunk ID: "
            f"{chunk['metadata']['chunk_id']}"
        )

        print(
            f"Distance: "
            f"{chunk['distance']}"
        )

        print(
            f"Score: "
            f"{chunk['score']}"
        )

        print("\nContent:")

        print(
            chunk["document"][:1000]
        )

        print(
            "\n" + "=" * 60 + "\n"
        )