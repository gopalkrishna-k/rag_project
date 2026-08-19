from vector_store import collection

print("=" * 80)
print("TOTAL DOCUMENTS")
print("=" * 80)

print(collection.count())

print("=" * 80)
print("ALL METADATA")
print("=" * 80)

results = collection.get(
    include=["metadatas"]
)

for metadata in results["metadatas"]:
    print(metadata)