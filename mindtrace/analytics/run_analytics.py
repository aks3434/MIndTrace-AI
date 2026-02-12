from typing import List
from mindtrace.core.types import Session
from mindtrace.nlp.embeddings import EmbeddingEncoder
from mindtrace.analytics.aggregator import aggregate_patterns

def analyze_sessions(
    sessions: List[Session],
    embedding_model
):
    encoder = EmbeddingEncoder(embedding_model)

    embeddings = {
        s.session_id: encoder.encode(s.text)
        for s in sessions
    }

    return aggregate_patterns(
        sessions=sessions,
        embeddings=embeddings
    )
