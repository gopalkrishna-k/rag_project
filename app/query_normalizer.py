import re
from difflib import SequenceMatcher

from query_analyzer import (
    ATTRIBUTE_PATTERNS,
    BIKE_NAMES,
    CATEGORY_PATTERNS,
)


MIN_FUZZY_SCORE = 0.86
MIN_FUZZY_WORD_LENGTH = 5


def _domain_phrases():
    """Build the correction vocabulary from the application's document domain."""

    phrases = set(BIKE_NAMES)

    for patterns in ATTRIBUTE_PATTERNS.values():
        phrases.update(patterns)

    for patterns in CATEGORY_PATTERNS.values():
        phrases.update(patterns)

    return sorted(
        phrases,
        key=lambda phrase: len(phrase.split()),
        reverse=True
    )


def _words(phrase: str):
    return re.findall(r"[A-Za-z]+|\d+", phrase)


def _is_conservative_match(question_words, candidate_words):
    """Accept only close, same-length matches with unchanged numeric tokens."""

    if len(question_words) != len(candidate_words):
        return False

    for question_word, candidate_word in zip(question_words, candidate_words):
        if question_word.isdigit() or candidate_word.isdigit():
            if question_word != candidate_word:
                return False

    question_text = " ".join(question_words).lower()
    candidate_text = " ".join(candidate_words).lower()

    if question_text == candidate_text:
        return False

    if (
        len(question_text.replace(" ", "")) < MIN_FUZZY_WORD_LENGTH
        or question_text[0] != candidate_text[0]
        or question_text[-1] != candidate_text[-1]
    ):
        return False

    return (
        SequenceMatcher(None, question_text, candidate_text).ratio()
        >= MIN_FUZZY_SCORE
    )


def normalize_question(question: str) -> str:
    """Conservatively correct domain terms before query analysis and retrieval."""

    matches = list(re.finditer(r"[A-Za-z]+|\d+", question))
    question_words = [match.group() for match in matches]
    replacements = []
    consumed_indexes = set()

    for phrase in _domain_phrases():
        candidate_words = _words(phrase)
        phrase_length = len(candidate_words)

        for start in range(len(question_words) - phrase_length + 1):
            indexes = range(start, start + phrase_length)

            if any(index in consumed_indexes for index in indexes):
                continue

            source_words = question_words[start:start + phrase_length]

            if not _is_conservative_match(source_words, candidate_words):
                continue

            replacements.append((
                matches[start].start(),
                matches[start + phrase_length - 1].end(),
                phrase
            ))
            consumed_indexes.update(indexes)

    normalized_question = question

    for start, end, replacement in reversed(replacements):
        normalized_question = (
            normalized_question[:start]
            + replacement
            + normalized_question[end:]
        )

    return normalized_question
