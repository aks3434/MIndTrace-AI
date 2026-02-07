import re
from collections import Counter

NEGATIONS = {"not", "never", "nothing", "no"}
CERTAINTY = {"always", "never", "every", "nothing", "can't"}

def extract_features(text: str) -> dict:
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return {}

    token_count = len(tokens)
    unique_ratio = len(set(tokens)) / token_count

    counts = Counter(tokens)

    return {
        "token_count": token_count,
        "unique_ratio": unique_ratio,
        "repetition_score": max(counts.values()) / token_count,
        "negation_freq": sum(counts[w] for w in NEGATIONS) / token_count,
        "certainty_freq": sum(counts[w] for w in CERTAINTY) / token_count,
        "question_ratio": text.count("?") / max(1, text.count(".")),
        "first_person_density": sum(counts[w] for w in {"i", "me", "my"}) / token_count,
    }
