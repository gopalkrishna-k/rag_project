from retriever import retrieve


questions = [
    "What type of brakes does the Bear 650 use?",
    "What is the fuel tank capacity of the Himalayan 450?",
    "Compare the Bear 650 and Himalayan 450.",
    "Which bike has the largest fuel tank?",
    "What is the capital of France?",
]


for question in questions:

    print("\n" + "=" * 100)
    print("QUESTION:")
    print(question)

    results = retrieve(question, top_k=3)

    if not results:

        print("\nâŒ NO RELEVANT CONTEXT FOUND")
        continue

    print("\nâœ… RETRIEVED CONTEXT")

    for result_index, result in enumerate(results):

        print(f"\n--- SEARCH RESULT GROUP {result_index + 1} ---")

        for i in range(len(result["documents"][0])):

            print(f"\nResult {i + 1}")
            print("Distance:")
            print(result["distances"][0][i])
            print("Metadata:")
            print(result["metadatas"][0][i])
            print("Document:")
            print(result["documents"][0][i][:300])
