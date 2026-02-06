from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class Observation:
    type: str
    tag: str
    session_ids: List[str]
    coherence: float
    signals: Dict[str, float]
    confidence:float
