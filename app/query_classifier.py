GLOBAL_PATTERNS = [
    "which bike",
    "which royal enfield",
    "what bike",
    "among the bikes",
    "among all bikes",
    "all bikes",
    "how many bikes",
    "average",
    "largest",
    "smallest",
    "highest",
    "lowest",
    "maximum",
    "minimum",
]


COMPARISON_PATTERNS = [
    "compare",
    "difference between",
    "better than",
    "which is better",
    "versus",
    "vs",
]


def classify_query(question: str) -> str:
    """
    Classify a question into a retrieval/query type.

    Returns:
        ENTITY
        COMPARISON
        GLOBAL
        UNKNOWN
    """

    question_lower = question.lower().strip()

    # Check comparison questions first
    for pattern in COMPARISON_PATTERNS:
        if pattern in question_lower:
            return "COMPARISON"

    # Check global questions
    for pattern in GLOBAL_PATTERNS:
        if pattern in question_lower:
            return "GLOBAL"

    # If no global/comparison pattern was found,
    # we currently treat it as an entity/normal query.
    return "ENTITY"