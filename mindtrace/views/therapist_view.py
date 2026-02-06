from typing import List
from mindtrace.core.observation import Observation

def therapist_summary(observations: List[Observation]):
    """
    Produces a neutral, high-level summary suitable for therapists
    or other professionals. No interpretation, no diagnosis.
    """
    return [
        {
            "topic": obs.tag,
            "sessions": len(obs.session_ids),
            "confidence": obs.confidence,
            "signals": list(obs.signals.keys()),
        }
        for obs in observations
    ]
