"""Module to normalize words."""


def normalize_word(word: str) -> str:
    """Set the word to lower and strip it.

    Args:
        word: word to normalize

    Returns:
        Normalized word
    """
    return word.lower().strip()
