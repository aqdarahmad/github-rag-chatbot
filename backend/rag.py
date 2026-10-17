import logging

from .retriever import retrieve
from .generator import generate_answer


logger = logging.getLogger("rag-chatbot")


# ==========================================
# Build Context
# ==========================================

def build_context(selected_chunks):

    context_parts = []

    for i, chunk in enumerate(selected_chunks):

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

    return "\n".join(context_parts)


# ==========================================
# Ask Question
# ==========================================

def ask(question):

    # Retrieve the closest chunks from ChromaDB
    selected_chunks = retrieve(
        query=question,
        top_k=8
    )

    # No results
    if not selected_chunks:

        return (
            "I could not find relevant "
            "information in the FastAPI "
            "documentation."
        )

    # Build context
    context = build_context(selected_chunks)

    logger.debug(
        "Sending context to Gemini:\n%s",
        context[:3000]
    )

    # Generate answer
    return generate_answer(question, context)
