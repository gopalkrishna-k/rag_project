from query_analyzer import analyze_query


questions = [
    "What is the fuel tank capacity of the Himalayan 450?",
    "How much fuel can the Himalayan 450 hold?",
    "What is the mileage of the Hunter 350?",
    "What type of brakes does the Bear 650 use?",
    "Compare the Bear 650 and Himalayan 450.",
    "What is the difference between Classic 350 and Hunter 350?",
    "Which Royal Enfield bike has the largest fuel tank?",
    "Which bike has the highest top speed?",
    "Which bike is the lightest?",
    "What is the average fuel tank capacity?",
    "How many bikes are in the document?",
    "Give me the fuel tank capacity of all bikes.",
    "What is the capital of France?",
]


for question in questions:

    result = analyze_query(question)

    print("=" * 80)
    print(question)
    print(result)