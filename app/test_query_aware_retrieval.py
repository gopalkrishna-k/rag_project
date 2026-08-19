from retriever import retrieve, format_context


questions = [
    "What is the fuel tank capacity of the Himalayan 450?",
    "What type of brakes does the Bear 650 use?",
    "Compare the Bear 650 and Himalayan 450.",
    "Which Royal Enfield bike has the largest fuel tank?",
]


for question in questions:

    print("=" * 100)
    print("QUESTION:")
    print(question)

    results = retrieve(question)

    print("\nCONTEXT:")
    print(format_context(results))