# core/pipeline.py

from typing import List, Dict, Optional

from mindtrace.core.types import Session
from mindtrace.core.observation import Observation

from mindtrace.analytics.aggregator import aggregate_patterns, build_render_payload
from mindtrace.core.llm_client import render_response


def run_mindtrace_pipeline(
    sessions: List[Session],
    embeddings: Dict[str, list],
) -> Optional[str]:
    """
    End-to-end MindTrace pipeline.

    Returns:
        - Rendered reflective response (str), or
        - None if no valid pattern is found
    """

    # 1️⃣ Aggregate patterns (pure analysis)
    observations: List[Observation] = aggregate_patterns(
        sessions=sessions,
        embeddings=embeddings,
    )

    if not observations:
        return None

    # 2️⃣ Select the strongest observation (deterministic)
    observation = _select_primary_observation(observations)

    # 3️⃣ Build render payload (projection only)
    payload = build_render_payload(
        observation=observation,
        sessions=sessions,
    )
    if payload is None:
        return None
    
    insight_text = render_response(payload)

    # 4️⃣ Render via LLM (language only)
    return {
        "payload": payload,
        "insight_text": insight_text,
    }

def _select_primary_observation(
    observations: List[Observation],
) -> Observation:
    """
    Selects the most reliable observation.
    Deterministic, no LLM, no heuristics explosion.
    """

    # Highest confidence wins
    observations = sorted(
        observations,
        key=lambda o: (o.confidence, len(o.session_ids)),
        reverse=True,
    )

    return observations[0]

