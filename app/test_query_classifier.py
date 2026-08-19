from query_classifier import classify_query


questions = [
    "What is the fuel tank capacity of the Himalayan 450?",
    "What is the mileage of the Hunter 350?",
    "Compare the Bear 650 and Himalayan 450.",
    "What is the difference between Classic 350 and Hunter 350?",
    "Which Royal Enfield bike has the largest fuel tank?",
    "Which bike has the highest top speed?",
    "Which bike has the smallest engine?",
    "What is the capital of France?",
]


for question in questions:

    query_type = classify_query(question)

    print("=" * 80)
    print("Question:", question)
    print("Query Type:", query_type)