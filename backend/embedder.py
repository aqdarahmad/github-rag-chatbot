"""Text embeddings.

Uses the all-MiniLM-L6-v2 model running on ONNX Runtime (the default embedding
function that ships with ChromaDB). It is the same model that the vector
database was built with, but it needs no PyTorch, so the app is small enough
to run on free hosting tiers (about 512 MB of RAM).

The same function is used to build the database (embeddings.py) and to embed
the user's question (retriever.py), so both always match.
"""

import threading

import numpy as np
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


_lock = threading.Lock()

_function = None


def _get_function():

    global _function

    with _lock:

        if _function is None:

            _function = DefaultEmbeddingFunction()

    return _function


def embed(texts):
    """Return L2-normalized embeddings (list of lists) for a list of texts."""

    vectors = np.array(
        _get_function()(list(texts)),
        dtype=np.float32
    )

    norms = np.linalg.norm(
        vectors,
        axis=1,
        keepdims=True
    )

    norms[norms == 0] = 1.0

    return (vectors / norms).tolist()
