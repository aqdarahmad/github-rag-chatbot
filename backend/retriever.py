import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)


logger = logging.getLogger("rag-chatbot")


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "github_code"


# ==========================================
# Embedding model
# ==========================================

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

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
    path=str(CHROMA_PATH),
    settings=Settings(anonymized_telemetry=False)
)

try:

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

except Exception as error:

    raise RuntimeError(
        f"ChromaDB collection '{COLLECTION_NAME}' was not "
        f"found in {CHROMA_PATH}. Build it first with: "
        f"python -m backend.github_documents && "
        f"python -m backend.embeddings"
    ) from error


# ==========================================
# Stage 1
# Semantic retrieval
# ==========================================

def search(query, top_k=20):

    # Convert the question to an embedding
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    # Semantic search
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

    logger.info(
        "ChromaDB returned %d candidates.",
        len(results["documents"][0])
    )

    return results


# ==========================================
# Stage 2
# Cross-Encoder reranking
# ==========================================

def rerank_chunks(results, query, max_chunks=5):

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]

    if not documents:

        return []

    # Score every (query, document) pair
    pairs = [
        [query, document]
        for document in documents
    ]

    scores = reranker.predict(pairs)

    # Build candidates
    chunks = [

        {
            "document": document,
            "metadata": metadata,
            "distance": float(distance),
            "rerank_score": float(score)
        }

        for document, metadata, distance, score in zip(
            documents,
            metadatas,
            distances,
            scores
        )
    ]

    # Highest reranker score = best
    chunks.sort(
        key=lambda chunk: chunk["rerank_score"],
        reverse=True
    )

    selected = chunks[:max_chunks]

    for i, chunk in enumerate(selected):

        logger.debug(
            "Result %d | %s | chunk %s | distance %.4f | rerank %.4f",
            i + 1,
            chunk["metadata"]["source"],
            chunk["metadata"]["chunk_id"],
            chunk["distance"],
            chunk["rerank_score"]
        )

    return selected


# ==========================================
# Full retrieval pipeline
# ==========================================

def retrieve(query, retrieval_k=20, final_k=5):

    results = search(
        query,
        top_k=retrieval_k
    )

    return rerank_chunks(
        results,
        query,
        max_chunks=final_k
    )


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

    print("\n==============================")
    print("Final Selected Chunks")
    print("==============================")

    for i, chunk in enumerate(chunks):

        print(f"\nResult {i + 1}")

        print(
            f"Source: {chunk['metadata']['source']}"
        )

        print(
            f"Reranker score: {chunk['rerank_score']:.4f}"
        )

        print()

        print(chunk["document"])

        print("\n" + "=" * 60)
