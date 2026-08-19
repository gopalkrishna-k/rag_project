from retriever import retrieve


questions = [
    "What is the fuel tank capacity of the Himalayan 450?",
    "What is the engine displacement of the Hunter 350?",
    "What is the top speed of the Classic 650?",
    "What type of brakes does the Bear 650 use?",
    "What is the seat height of the Interceptor 650?",
    "What is the capital of France?",
    "Who won the FIFA World Cup in 2022?",
    "What is the population of India?",
    "How do I make chicken biryani?",
    "What is the Python programming language?",
]


for question in questions:
    results = retrieve(question, top_k=3)
    print("=" * 100)
    print("QUESTION:")
    print(question)

    if results is None:
        print("\nâŒ REJECTED")
        print("This question is not relevant to the document.")
    else:
        print("\nâœ… ACCEPTED")
        print("\nBest result:")
        print(results["metadatas"][0][0])
        print("\nDistance:")
        print(results["distances"][0][0])
