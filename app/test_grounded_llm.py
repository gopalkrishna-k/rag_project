from prompt import build_rag_prompt
from llm import generate_answer


question = "What is the capital of France?"

context = """
Bike: Himalayan 450

Fuel tank: 17.0 L

Engine: 451.65 cc single-cylinder, liquid-cooled, DOHC, 4-valve

Maximum power: 40.02 PS @ 8,000 rpm
"""


prompt = build_rag_prompt(question, context)

answer = generate_answer(prompt)


print("=" * 80)
print("QUESTION")
print("=" * 80)
print(question)

print("=" * 80)
print("ANSWER")
print("=" * 80)
print(answer)
