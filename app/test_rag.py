from query_analyzer import analyze_query
from query_normalizer import normalize_question
from retriever import retrieve, format_context


DEBUG_SEPARATOR = "=" * 50
DEBUG = False


def print_debug(title: str, value):
    if not DEBUG:
        return

    print("\n" + DEBUG_SEPARATOR)
    print(title)
    print(DEBUG_SEPARATOR)
    print(value)


def build_test_prompt(question: str, context: str) -> str:
    return f"""
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


def answer_question(question: str):
    original_question = question
    normalized_question = normalize_question(original_question)

    print_debug("ORIGINAL QUESTION", original_question)
    print_debug("NORMALIZED QUESTION", normalized_question)

    # Reuse the existing query-aware RAG pipeline.
    analysis = analyze_query(normalized_question)
    print_debug("QUERY ANALYSIS", analysis)

    results = retrieve(normalized_question)
    print_debug("RETRIEVED RESULTS", results)

    context = format_context(results)
    print_debug("FORMATTED CONTEXT", context)

    if not results:
        print("No relevant context found in the document.")
        return

    prompt = build_test_prompt(original_question, context)
    print_debug("LLM PROMPT", prompt)

    try:
        # Import here so a missing API key is reported without ending the
        # interactive testing session.
        from llm import generate_answer

        answer = generate_answer(prompt)
    except Exception as error:
        print(f"\nUnable to generate an answer: {error}")
        return

    print(f"\n{answer}")


def main():
    while True:
        try:
            question = input(
                "\nEnter your question (or type 'exit' to quit):\n> "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting RAG application test.")
            break

        if not question:
            print("Please enter a question.")
            continue

        if question.lower() in {"exit", "quit"}:
            print("Exiting RAG application test.")
            break

        answer_question(question)


if __name__ == "__main__":
    main()
