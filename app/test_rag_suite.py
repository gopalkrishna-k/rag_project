from retriever import retrieve, format_context
from llm import generate_answer


# ============================================================
# TEST QUESTIONS
# ============================================================

TEST_CASES = [

    # ========================================================
    # ENTITY QUESTIONS
    # ========================================================

    {
        "category": "ENTITY",
        "question": "What is the fuel tank capacity of the Himalayan 450?"
    },

    {
        "category": "ENTITY",
        "question": "How much fuel can the Himalayan 450 hold?"
    },

    {
        "category": "ENTITY",
        "question": "What is the engine displacement of the Hunter 350?"
    },

    {
        "category": "ENTITY",
        "question": "How many cc is the Hunter 350?"
    },

    {
        "category": "ENTITY",
        "question": "What type of brakes does the Bear 650 use?"
    },

    {
        "category": "ENTITY",
        "question": "What is the seat height of the Interceptor 650?"
    },

    {
        "category": "ENTITY",
        "question": "What is the mileage of the Continental GT 650?"
    },


    # ========================================================
    # PARAPHRASED QUESTIONS
    # ========================================================

    {
        "category": "PARAPHRASE",
        "question": "Which bike can carry the most fuel?"
    },

    {
        "category": "PARAPHRASE",
        "question": "Which Royal Enfield has the biggest fuel tank?"
    },

    {
        "category": "PARAPHRASE",
        "question": "Which motorcycle sits the lowest from the ground?"
    },

    {
        "category": "PARAPHRASE",
        "question": "Which bike produces the most power?"
    },

    {
        "category": "PARAPHRASE",
        "question": "Which Royal Enfield has the largest engine?"
    },


    # ========================================================
    # COMPARISON QUESTIONS
    # ========================================================

    {
        "category": "COMPARISON",
        "question": "Compare the Bear 650 and Himalayan 450."
    },

    {
        "category": "COMPARISON",
        "question": "Which is better for fuel capacity, Bear 650 or Himalayan 450?"
    },

    {
        "category": "COMPARISON",
        "question": "Compare the seat heights of the Classic 650 and Interceptor 650."
    },

    {
        "category": "COMPARISON",
        "question": "Compare the engine displacement of the Hunter 350 and Himalayan 450."
    },

    {
        "category": "COMPARISON",
        "question": "Which has more power, Bear 650 or Himalayan 450?"
    },


    # ========================================================
    # GLOBAL QUESTIONS
    # ========================================================

    {
        "category": "GLOBAL",
        "question": "Which Royal Enfield bike has the largest fuel tank?"
    },

    {
        "category": "GLOBAL",
        "question": "Which bike has the highest top speed?"
    },

    {
        "category": "GLOBAL",
        "question": "Which bike has the lowest seat height?"
    },

    {
        "category": "GLOBAL",
        "question": "Which bike has the highest engine displacement?"
    },

    {
        "category": "GLOBAL",
        "question": "Which bike has the longest wheelbase?"
    },

    {
        "category": "GLOBAL",
        "question": "Which bike has the highest ground clearance?"
    },


    # ========================================================
    # OUT-OF-CONTEXT QUESTIONS
    # ========================================================

    {
        "category": "OUT_OF_CONTEXT",
        "question": "What is the capital of France?"
    },

    {
        "category": "OUT_OF_CONTEXT",
        "question": "Who won the FIFA World Cup in 2022?"
    },

    {
        "category": "OUT_OF_CONTEXT",
        "question": "How do I make chicken biryani?"
    },

    {
        "category": "OUT_OF_CONTEXT",
        "question": "What is the Python programming language?"
    },

    {
        "category": "OUT_OF_CONTEXT",
        "question": "Who is the Prime Minister of India?"
    },


    # ========================================================
    # POTENTIAL HALLUCINATION QUESTIONS
    # Information should NOT be invented if absent.
    # ========================================================

    {
        "category": "MISSING_INFORMATION",
        "question": "What is the exact 0 to 100 km/h acceleration time of the Himalayan 450?"
    },

    {
        "category": "MISSING_INFORMATION",
        "question": "What is the exact horsepower of the Classic 650 at 5000 RPM?"
    },

    {
        "category": "MISSING_INFORMATION",
        "question": "What is the exact service cost of the Bear 650?"
    },

    {
        "category": "MISSING_INFORMATION",
        "question": "What is the insurance cost of the Himalayan 450?"
    },


    # ========================================================
    # SIMILAR ENTITY NAMES
    # ========================================================

    {
        "category": "ENTITY_ACCURACY",
        "question": "What is the fuel tank capacity of the Classic 650?"
    },

    {
        "category": "ENTITY_ACCURACY",
        "question": "What is the fuel tank capacity of the Classic 350?"
    },

    {
        "category": "ENTITY_ACCURACY",
        "question": "What is the fuel tank capacity of the Interceptor 650?"
    },

    {
        "category": "ENTITY_ACCURACY",
        "question": "What is the fuel tank capacity of the Meteor 350?"
    },


    # ========================================================
    # MULTI-ATTRIBUTE QUESTIONS
    # ========================================================

    {
        "category": "MULTI_ATTRIBUTE",
        "question": "Tell me the engine, fuel tank capacity, mileage and seat height of the Himalayan 450."
    },

    {
        "category": "MULTI_ATTRIBUTE",
        "question": "Give me the power, torque, brakes and fuel tank capacity of the Bear 650."
    },

    {
        "category": "MULTI_ATTRIBUTE",
        "question": "What are the engine displacement, mileage and top speed of the Hunter 350?"
    },
]


# ============================================================
# RUN TESTS
# ============================================================

def run_test(question):

    print("\n" + "=" * 100)
    print("QUESTION:")
    print(question)
    print("=" * 100)

    try:

        results = retrieve(question)

        if not results:

            print("\n❌ NO RELEVANT CONTEXT FOUND")

            return

        context = format_context(results)

        print("\n✅ CONTEXT RETRIEVED")

        answer = generate_answer(
            f"""
Answer the user's question using ONLY the information
provided in the context.

If the answer is not present in the context,
say that the information is not available in the document.

Do not use outside knowledge.

CONTEXT:
{context}

QUESTION:
{question}
"""
        )

        print("\nFINAL ANSWER:")
        print(answer)

    except Exception as e:

        print("\n❌ ERROR:")
        print(type(e).__name__)
        print(e)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 100)
    print("RAG APPLICATION TEST SUITE")
    print("=" * 100)

    print(f"\nTotal test cases: {len(TEST_CASES)}")

    for index, test_case in enumerate(TEST_CASES, start=1):

        print("\n")
        print("#" * 100)
        print(
            f"TEST {index}/{len(TEST_CASES)}"
        )
        print(
            f"CATEGORY: {test_case['category']}"
        )
        print("#" * 100)

        run_test(
            test_case["question"]
        )