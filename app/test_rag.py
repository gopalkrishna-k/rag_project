from query_analyzer import analyze_query
from retriever import retrieve, format_context
from llm import generate_answer


# --------------------------------------------------
# TEST QUESTION
# --------------------------------------------------

question = "what is the capital of india?"


# --------------------------------------------------
# STEP 1: ANALYZE QUERY
# --------------------------------------------------

analysis = analyze_query(question)


# --------------------------------------------------
# STEP 2: RETRIEVE RELEVANT DOCUMENTS
# --------------------------------------------------

results = retrieve(question)


# --------------------------------------------------
# STEP 3: FORMAT RETRIEVED CONTEXT
# --------------------------------------------------

context = format_context(results)


# --------------------------------------------------
# STEP 4: BUILD LLM PROMPT
# --------------------------------------------------

prompt = f"""
You are a helpful assistant that answers questions about
Royal Enfield motorcycles.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided document."

Do not invent or assume information.

Keep the answer clear and concise.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""


# --------------------------------------------------
# STEP 5: GENERATE FINAL ANSWER
# --------------------------------------------------

answer = generate_answer(prompt)


# --------------------------------------------------
# FINAL OUTPUT
# --------------------------------------------------

print()
print("=" * 80)
print("QUESTION")
print("=" * 80)
print(question)

print()
print("=" * 80)
print("FINAL ANSWER")
print("=" * 80)
print(answer)

print()