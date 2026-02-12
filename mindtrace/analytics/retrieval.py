from typing import List
from sentence_transformers import SentenceTransformer

from mindtrace.storage.vector_store import MindTraceVectorStore
from mindtrace.storage.session_store import load_sessions
from mindtrace.core.types import Session


def retrieve_candidate_sessions(
    user_id: str,
    query_text: str,
    top_k: int = 10,
) -> List[Session]:
    """
    Retrieve candidate sessions using semantic similarity.
    This does NOT perform any reasoning or aggregation.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vector_store = MindTraceVectorStore()

    query_embedding = model.encode(query_text).tolist()

    session_ids = vector_store.query_similar_sessions(
        user_id=user_id,
        query_embedding=query_embedding,
        top_k=top_k,
    )

    # Load full sessions from factual store
    all_sessions = load_sessions()
    session_map = {s.session_id: s for s in all_sessions}

    return [session_map[sid] for sid in session_ids if sid in session_map]
