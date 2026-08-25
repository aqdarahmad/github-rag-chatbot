import chromadb

from pathlib import Path

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"


# ==========================================
# Embedding model
# ==========================================

EMBEDDING_MODEL_NAME = (
    "all-MiniLM-L6-v2"
)

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


# ==========================================
# Reranker
# ==========================================

RERANKER_MODEL_NAME = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

reranker = CrossEncoder(
    RERANKER_MODEL_NAME
)


# ==========================================
# ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    name="github_code"
)


# ==========================================
# Stage 1
# Semantic retrieval
# ==========================================

def search(
    query,
    top_k=20
):

    print(
        "\nSearching ChromaDB..."
    )

    # --------------------------------------
    # Convert question to embedding
    # --------------------------------------

    query_embedding = (
        embedding_model.encode(
            query,
            normalize_embeddings=True
        )
    )

    # --------------------------------------
    # Semantic search
    # --------------------------------------

    results = collection.query(

        query_embeddings=[
            query_embedding.tolist()
        ],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results[
        "documents"
    ][0]

    print(
        f"ChromaDB returned "
        f"{len(documents)} candidates."
    )

    return results


# ==========================================
# Stage 2
# Cross-Encoder reranking
# ==========================================

def rerank_chunks(
    results,
    query,
    max_chunks=5
):

    documents = results[
        "documents"
    ][0]

    metadatas = results[
        "metadatas"
    ][0]

    distances = results[
        "distances"
    ][0]

    if not documents:

        return []

    # ======================================
    # Create query-document pairs
    # ======================================

    pairs = [

        [
            query,
            document
        ]

        for document in documents
    ]

    # ======================================
    # Reranker scores
    # ======================================

    scores = reranker.predict(
        pairs
    )

    # ======================================
    # Build candidates
    # ======================================

    chunks = []

    for document, metadata, distance, score in zip(
        documents,
        metadatas,
        distances,
        scores
    ):

        chunks.append({

            "document": document,

            "metadata": metadata,

            "distance": float(
                distance
            ),

            "rerank_score": float(
                score
            )

        })

    # ======================================
    # Highest reranker score = best
    # ======================================

    chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    selected = chunks[
        :max_chunks
    ]

    # ======================================
    # Debug output
    # ======================================

    print(
        "\n=============================="
    )

    print(
        "Reranked Results"
    )

    print(
        "=============================="
    )

    for i, chunk in enumerate(
        selected
    ):

        print(
            f"\nResult {i + 1}"
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
            f"Chroma distance: "
            f"{chunk['distance']:.4f}"
        )

        print(
            f"Reranker score: "
            f"{chunk['rerank_score']:.4f}"
        )

        print(
            "\nContent:"
        )

        print(
            chunk["document"][:700]
        )

    return selected


# ==========================================
# Full retrieval pipeline
# ==========================================

def retrieve(
    query,
    retrieval_k=20,
    final_k=5
):

    results = search(
        query,
        top_k=retrieval_k
    )

    selected_chunks = rerank_chunks(
        results,
        query,
        max_chunks=final_k
    )

    return selected_chunks


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about FastAPI: "
    )

    chunks = retrieve(
        question,
        retrieval_k=20,
        final_k=5
    )

    print(
        "\n=============================="
    )

    print(
        "Final Selected Chunks"
    )

    print(
        "=============================="
    )

    for i, chunk in enumerate(
        chunks
    ):

        print(
            f"\nResult {i + 1}"
        )

        print(
            chunk["document"]
        )

        print(
            "\n" + "=" * 60
        )