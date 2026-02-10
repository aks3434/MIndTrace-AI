from dataclasses import dataclass

@dataclass(frozen=True)
class RenderPayload:
    topic: str
    session_count: int
    time_range: str
    confidence: float
    evidence_summary: str
    descriptive_markers: list[str]
