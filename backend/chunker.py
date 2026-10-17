
import os
import re
from pathlib import Path


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = BASE_DIR / "data"


# ==========================================
# Configuration
# ==========================================

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

SUPPORTED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
}


# ==========================================
# Generic text splitting
# ==========================================

def split_large_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
):
    """
    Split large text into overlapping chunks.

    Used when a logical section is too large.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# ==========================================
# Markdown chunking
# ==========================================

def chunk_markdown(text: str):
    """
    Split Markdown according to headings.

    Each heading and its content stay together
    whenever possible.
    """

    heading_pattern = r"(?m)^(#{1,6})\s+.+$"

    matches = list(
        re.finditer(
            heading_pattern,
            text
        )
    )

    if not matches:
        return split_large_text(text)

    sections = []

    # Content before first heading
    if matches[0].start() > 0:

        preamble = text[:matches[0].start()].strip()

        if preamble:
            sections.append(preamble)

    # Extract sections
    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if section:
            sections.append(section)

    # Split only large sections
    chunks = []

    for section in sections:

        if len(section) <= CHUNK_SIZE:

            chunks.append(section)

        else:

            chunks.extend(
                split_large_text(section)
            )

    return chunks


# ==========================================
# Python code chunking
# ==========================================

def chunk_python(text: str):
    """
    Split Python code using top-level definitions.

    Keeps functions/classes together whenever possible.
    """

    lines = text.splitlines()

    chunks = []

    current = []

    # Detect top-level Python definitions
    definition_pattern = re.compile(
        r"^(class|def|async\s+def)\s+"
    )

    for line in lines:

        is_definition = (
            definition_pattern.match(line)
            and not line.startswith((" ", "\t"))
        )

        if is_definition and current:

            chunk = "\n".join(current).strip()

            if chunk:
                chunks.append(chunk)

            current = []

        current.append(line)

    # Last chunk
    if current:

        chunk = "\n".join(current).strip()

        if chunk:
            chunks.append(chunk)

    # Split oversized functions/classes
    final_chunks = []

    for chunk in chunks:

        if len(chunk) <= CHUNK_SIZE:

            final_chunks.append(chunk)

        else:

            final_chunks.extend(
                split_large_text(chunk)
            )

    return final_chunks


# ==========================================
# Generic file chunking
# ==========================================

def chunk_text(text: str, filename: str):

    extension = Path(filename).suffix.lower()

    if extension == ".md":

        return chunk_markdown(text)

    if extension == ".py":

        return chunk_python(text)

    return split_large_text(text)


# ==========================================
# Load documents
# ==========================================

def load_documents():

    documents = []

    for root, dirs, files in os.walk(DATA_DIRECTORY):

        for filename in files:

            file_path = Path(root) / filename

            # Ignore unsupported files
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

            except UnicodeDecodeError:

                print(
                    f"Skipping non-text file: {file_path}"
                )

                continue

            chunks = chunk_text(
                text,
                filename
            )

            for index, chunk in enumerate(chunks):

                documents.append({

                    "text": chunk,

                    "source": file_path.relative_to(
                        BASE_DIR
                    ).as_posix(),

                    "chunk_id": index,

                    "file_type": file_path.suffix.lower()

                })

    return documents


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    documents = load_documents()

    print(
        f"\nTotal chunks: {len(documents)}"
    )

    print(
        "\nFirst 10 chunks:"
    )

    print(
        "=" * 80
    )

    for document in documents[:10]:

        print(
            f"\nSource: {document['source']}"
        )

        print(
            f"Chunk ID: {document['chunk_id']}"
        )

        print(
            f"Type: {document['file_type']}"
        )

        print(
            "-" * 80
        )

        print(
            document["text"][:1000]
        )

        print(
            "=" * 80
        )

