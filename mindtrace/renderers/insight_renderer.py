def render(obs):
    lines = []

    # Base observation (always safe)
    lines.append(
        "A similar concern appears across multiple sessions."
    )

    # Linguistic signals
    if "certainty_freq" in obs.signals:
        lines.append(
            "The language used around this concern has become more absolute."
        )

    if "unique_ratio" in obs.signals and obs.signals["unique_ratio"] < 0:
        lines.append(
            "The way this concern is described shows limited variation."
        )

    # Confidence-based reinforcement (VERY IMPORTANT: last)
    if obs.confidence >= 0.75:
        lines.append(
            "This pattern appears consistently over time."
        )

    return " ".join(lines)
