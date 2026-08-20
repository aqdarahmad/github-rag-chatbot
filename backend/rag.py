from .retriever import search, select_relevant_chunks
from .generator import generate_answer


# ==========================================
# Build Context
# ==========================================

def build_context(selected_chunks):

    context_parts = []

    for i, chunk in enumerate(selected_chunks):

        context_parts.append(
            f"""
--- Context {i + 1} ---
Source: {chunk["metadata"]["source"]}
Chunk ID: {chunk["metadata"]["chunk_id"]}

{chunk["document"]}
"""
        )

    return "\n".join(context_parts)


# ==========================================
# Ask Question
# ==========================================

def ask(question):

    print("\nSearching ChromaDB...")

    # ======================================
    # Retrieve 20 chunks
    # ======================================

    results = search(
        question,
        top_k=20
    )

    # ======================================
    # Select best 5 chunks
    # ======================================

    selected_chunks = select_relevant_chunks(
        results,
        question,
        max_chunks=5
    )

    # ======================================
    # Display selected chunks
    # ======================================

    print("\nSelected relevant chunks:")
    print("==============================")

    for i, chunk in enumerate(selected_chunks):

        print(f"\nResult {i + 1}")

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
            chunk["document"][:500]
        )

    # ======================================
    # Build context from selected chunks
    # ======================================

    context = build_context(
        selected_chunks
    )

    print("\n==============================")
    print("Sending context to Gemini...")
    print("==============================")

    print(
        context[:3000]
    )

    # ======================================
    # Generate answer
    # ======================================

    answer = generate_answer(
        question,
        context
    )

    return answer


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about FastAPI: "
    )

    answer = ask(question)

    print("\n==============================")
    print("Final Answer")
    print("==============================\n")

    print(answer)