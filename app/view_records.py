from vector_store import collection

records = collection.get(
    ids=["chunk_7"],
    include=["documents", "metadatas", "embeddings"]
)

print("ID:")
print(records["ids"][0])

print("\nDOCUMENT:")
print(records["documents"][0])

print("\nMETADATA:")
print(records["metadatas"][0])

print("\nFIRST 10 EMBEDDING VALUES:")
print(records["embeddings"][0][:10])
