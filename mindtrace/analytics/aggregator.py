from typing import List, Dict, Optional
from collections import defaultdict
from datetime import timedelta
from mindtrace.core.types import Session
from mindtrace.nlp.features import extract_features
from mindtrace.nlp.embeddings import cosine_similarity
from mindtrace.core.observation import Observation
from mindtrace.core.schemas.render_payload import RenderPayload


# ---- Tunables (conservative but realistic) ----
MIN_CHAIN_LENGTH = 3          # at least 3 sessions to form a chain
MIN_AVG_COHERENCE = 0.45      # average semantic coherence across the chain
MIN_FEATURE_SIGNALS = 2       # number of feature deltas required
DELTA_THRESHOLD = 0.05        # per-feature significance threshold


def _group_by_confirmed_tag(sessions: List[Session]) -> Dict[str, List[Session]]:
    """
    Groups sessions by user-confirmed tags.
    Sessions with multiple tags appear in multiple groups.
    """
    buckets: Dict[str, List[Session]] = defaultdict(list)
    for s in sessions:
        for tag in s.confirmed_tags:
            buckets[tag].append(s)

    # ensure chronological order per tag
    for tag in buckets:
        buckets[tag].sort(key=lambda x: x.started_at)

    return buckets


def _average_coherence(
    sessions: List[Session],
    embeddings: Dict[str, list],
) -> float:
    """
    Computes average pairwise cosine similarity across a chain.
    """
    sims = []
    for i, s1 in enumerate(sessions):
        for s2 in sessions[i + 1:]:
            sims.append(
                cosine_similarity(
                    embeddings[s1.session_id],
                    embeddings[s2.session_id],
                )
            )
    return sum(sims) / len(sims) if sims else 0.0


def _feature_drift(
    start_text: str,
    end_text: str,
) -> Dict[str, float]:
    """
    Computes feature deltas between first and last session only.
    """
    f_start = extract_features(start_text)
    f_end = extract_features(end_text)

    deltas = {}
    for k in f_start.keys() & f_end.keys():
        delta = f_end[k] - f_start[k]
        if abs(delta) > DELTA_THRESHOLD:
            deltas[k] = delta

    return deltas

def compute_confidence(chain_length: int, coherence: float) -> float:
    """Deterministic confidence score.
    - Increase with evidence (chain length)
    - Increase with sementic consistency
    - Capped to avoid false authority    
    """
    base = 0.3
    length_bonus = min(0.3, 0.05 * chain_length)
    coherence_bonus = min(0.4, coherence)

    return round(min(1.0, base + length_bonus + coherence_bonus), 2)

def aggregate_patterns(
    sessions: List[Session],
    embeddings: Dict[str, list],
) -> List[dict]:
    """
    Produces chain-based observations:
    - groups by confirmed tag
    - requires 3+ sessions
    - checks average semantic coherence
    - checks linguistic feature drift (first -> last)
    """
    observations = []

    by_tag = _group_by_confirmed_tag(sessions)

    for tag, chain in by_tag.items():
        if len(chain) < MIN_CHAIN_LENGTH:
            continue

        coherence = _average_coherence(chain, embeddings)
        if coherence < MIN_AVG_COHERENCE:
            continue

        deltas = _feature_drift(chain[0].text, chain[-1].text)
        if len(deltas) < MIN_FEATURE_SIGNALS:
            continue
        
        confidence = compute_confidence(len(chain) ,coherence)
        observations.append(
            Observation(
                type="recurring_chain",
                tag=tag,
                session_ids=[s.session_id for s in chain],
                coherence=round(coherence, 3),
                signals=deltas,
                confidence=confidence,
            )
        )


    return observations

def _describe_time_range(sessions: List[Session]) -> str:
    """
    Returns a human-readable description of the time span
    covered by the given sessions.
    """

    if not sessions:
        return "over an unknown time span"

    if len(sessions) == 1:
        return "within a single session"

    start = sessions[0].started_at
    end = sessions[-1].started_at
    days = max((end - start).days, 1)

    if days < 7:
        return f"over the past {days} days"
    elif days < 30:
        weeks = days // 7
        return f"over the past {weeks} weeks"
    else:
        months = days // 30
        return f"over the past {months} months"

def _summarize_evidence(
    observation: Observation,
    sessions: List[Session],
) -> str:
    """
    Produces a neutral evidence summary based strictly
    on verified observations.
    """

    return (
        f"Across {len(sessions)} sessions tagged as '{observation.tag}', "
        "the same theme appears repeatedly with consistent semantic patterns. "
        f"The system detected a recurring chain with a confidence score of "
        f"{observation.confidence}."
    )

def extract_descriptive_markers(
    observation: Observation,
    sessions: list[Session],
) -> list[str]:
    markers = []

    if "future" in observation.signals:
        markers.append("often discussed in relation to future-oriented concerns")

    if "self_reference" in observation.signals:
        markers.append("frequently expressed using first-person language")

    if observation.coherence > 0.7:
        markers.append("described in a consistent way across multiple sessions")

    return markers



def build_render_payload(
    observation: Observation,
    sessions: List[Session],
) -> RenderPayload:
    """
    Converts a verified Observation into a RenderPayload.
    This is a projection step, not reasoning.
    """

    relevant_sessions = [
        s for s in sessions
        if s.session_id in observation.session_ids
    ]

    time_range = _describe_time_range(relevant_sessions)

    evidence_summary = _summarize_evidence(
        observation=observation,
        sessions=relevant_sessions,
    )

    descriptive_markers = extract_descriptive_markers(
        observation=observation,
        sessions=relevant_sessions,
    )

    return RenderPayload(
        topic=observation.tag,
        session_count=len(relevant_sessions),
        time_range=time_range,
        confidence=observation.confidence,
        evidence_summary=evidence_summary,
        descriptive_markers=descriptive_markers,
    )
