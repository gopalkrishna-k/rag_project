from entity_detector import detect_bikes


questions = [
    "What type of brakes does the Bear 650 use?",
    "What is the fuel tank capacity of the Himalayan 450?",
    "Tell me the mileage of Hunter 350.",
    "Compare the Bear 650 and Himalayan 450.",
    "What is the capital of France?"
]


for question in questions:
    bikes = detect_bikes(question)
    print("=" * 80)
    print("Question:", question)
    print("Detected bikes:", bikes)
