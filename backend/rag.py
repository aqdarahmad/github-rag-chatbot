from .retriever import retrieve
from .generator import generate_answer


# ==========================================
# Build Context
# ==========================================

def build_context(selected_chunks):

    context_parts = []

    for i, chunk in enumerate(
        selected_chunks
    ):

        context_parts.append(

            f"""
--- Context {i + 1} ---

Source:
{chunk["metadata"]["source"]}

Chunk ID:
{chunk["metadata"]["chunk_id"]}

{chunk["document"]}
"""
        )

    return "\n".join(
        context_parts
    )


# ==========================================
# Ask Question
# ==========================================

def ask(question):

    # ======================================
    # Retrieve + Rerank
    # ======================================

    selected_chunks = retrieve(

        query=question,

        retrieval_k=20,

        final_k=5
    )

    # ======================================
    # No results
    # ======================================

    if not selected_chunks:

        return (
            "I could not find relevant "
            "information in the FastAPI "
            "documentation."
        )

    # ======================================
    # Build context
    # ======================================

    context = build_context(
        selected_chunks
    )

    print(
        "\n=============================="
    )

    print(
        "Sending context to Gemini..."
    )

    print(
        "=============================="
    )

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