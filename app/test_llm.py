from llm import generate_answer


prompt = """
Explain in simple terms what a motorcycle engine is.
"""


answer = generate_answer(prompt)


print("=" * 80)
print("GEMINI RESPONSE")
print("=" * 80)

print(answer)
