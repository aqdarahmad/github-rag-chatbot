import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_collection(name="github_code")

all_docs = collection.get(
    where={"source": {"$eq": "../data\\docs\\en\\docs\\tutorial\\path-params.md"}}
)

for i, doc in enumerate(all_docs['documents']):
    print(f"[Chunk {all_docs['metadatas'][i]['chunk_id']}] {doc[:200]}")
    print("---")