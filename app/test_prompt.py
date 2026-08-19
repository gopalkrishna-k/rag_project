from prompt import build_rag_prompt


question = "What is the fuel tank capacity of the Himalayan 450?"

context = """
Bike: Himalayan 450

Fuel tank: 17.0 L

Engine: 451.65 cc single-cylinder, liquid-cooled, DOHC, 4-valve

Maximum power: 40.02 PS @ 8,000 rpm
"""


prompt = build_rag_prompt(question, context)

print("=" * 80)
print("GENERATED PROMPT")
print("=" * 80)

print(prompt)
