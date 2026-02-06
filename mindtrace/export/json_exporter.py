def export_observation(obs):
    return {
        "type": obs.type,
        "tag": obs.tag,
        "session_ids": obs.session_ids,
        "coherence": obs.coherence,
        "confidence": obs.confidence,
        "signals": obs.signals,
    }
