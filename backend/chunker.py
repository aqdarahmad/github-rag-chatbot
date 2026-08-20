import os
import re


DATA_DIRECTORY = "../data"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


def split_large_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split a long section into smaller overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks


def chunk_markdown(text):
    """
    Split Markdown according to headings.

    Each Markdown section stays together as much as possible.
    """

    # Match Markdown headings:
    # # Heading
    # ## Heading
    # ### Heading
    heading_pattern = r"(?m)^(#{1,6})\s+.+$"

    matches = list(re.finditer(heading_pattern, text))

    # If there are no headings, use normal chunking
    if not matches:
        return split_large_text(text)

    sections = []

    # Content before the first heading
    if matches[0].start() > 0:

        preamble = text[:matches[0].start()].strip()

        if preamble:
            sections.append(preamble)

    # Create sections
    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        if section:
            sections.append(section)

    # Split only sections that are too large
    chunks = []

    for section in sections:

        if len(section) <= CHUNK_SIZE:

            chunks.append(section)

        else:

            chunks.extend(
                split_large_text(section)
            )

    return chunks


def chunk_text(text, filename):

    # Markdown files
    if filename.lower().endswith(".md"):

        return chunk_markdown(text)

    # Other text/code files
    return split_large_text(text)


def load_documents():

    documents = []

    for root, dirs, files in os.walk(DATA_DIRECTORY):

        for filename in files:

            file_path = os.path.join(
                root,
                filename
            )

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read()

                chunks = chunk_text(
                    text,
                    filename
                )

                for index, chunk in enumerate(chunks):

                    documents.append({
                        "text": chunk,
                        "source": file_path,
                        "chunk_id": index
                    })

            except UnicodeDecodeError:

                print(
                    f"Skipping non-text file: {file_path}"
                )

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(
        f"Total chunks: {len(documents)}"
    )

    for document in documents[:5]:

        print("\n==============================")

        print(
            f"Source: {document['source']}"
        )

        print(
            f"Chunk ID: {document['chunk_id']}"
        )

        print(
            document["text"][:1000]
        )