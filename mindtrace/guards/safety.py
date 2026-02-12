FORBIDDEN = [
    "you are",
    "this means",
    "diagnos",
    "mental health",
    "disorder",
]

MAX_SENTENCES = 4


def _sentence_count(text: str) -> int:
    # Count non-empty sentences robustly
    return len([s for s in text.split(".") if s.strip()])


def assert_safe(text: str):
    if _sentence_count(text) > MAX_SENTENCES:
        raise ValueError("Output too interpretive")

    lower = text.lower()
    for phrase in FORBIDDEN:
        if phrase in lower:
            raise ValueError(f"Unsafe phrase: {phrase}")
