from retriever import retrieve


query = "What type of brakes does the Bear 650 use?"

results = retrieve(
    query,
    bike="Bear 650",
    top_k=3
)


print("=" * 100)
print("QUERY")
print("=" * 100)
print(query)


if results is None:
    print("\nâŒ No relevant result found.")
else:
    print("\nâœ… RESULTS")
    for i in range(len(results["documents"][0])):
        print(f"\nRESULT {i + 1}")
        print("-" * 80)
        print("Distance:")
        print(results["distances"][0][i])
        print("\nMetadata:")
        print(results["metadatas"][0][i])
        print("\nDocument:")
        print(results["documents"][0][i])
