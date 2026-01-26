# core/patterns.py

from dataclasses import dataclass, field
from typing import List, Optional

from mindtrace.core.memory_schemas import BehavioralMemory


# =================================================
# OUTPUT CONTRACT
# =================================================

@dataclass
class PatternResult:
    spiral_detected: bool = False
    emotional_trend: Optional[str] = None  # improving | declining | stable
    rumination_detected: bool = False
    absolutist_escalation: bool = False
    risk_level: str = "low"  # low | medium
    dominant_signals: List[str] = field(default_factory=list)


# =================================================
# HELPERS
# =================================================

def last_n(memories: List[BehavioralMemory], n: int) -> List[BehavioralMemory]:
    return memories[-n:] if len(memories) >= n else memories


# =================================================
# PATTERN RULES
# =================================================

def detect_spiral(
    history: List[BehavioralMemory],
    current: BehavioralMemory,
    window: int = 6,
) -> bool:
    """
    Spiral = sustained high repetition over multiple sessions.
    """
    recent = last_n(history, window)
    recent_scores = [m.repetition_score for m in recent] + [current.repetition_score]

    high_repetition = [s for s in recent_scores if s >= 0.8]

    return len(high_repetition) >= 3


def detect_emotional_trend(
    history: List[BehavioralMemory],
) -> Optional[str]:
    """
    Trend based on sentiment score movement.
    """
    if len(history) < 6:
        return None

    earlier = history[-6:-3]
    recent = history[-3:]

    earlier_avg = sum(m.sentiment_score for m in earlier) / 3
    recent_avg = sum(m.sentiment_score for m in recent) / 3

    if recent_avg < earlier_avg - 0.1:
        return "declining"
    elif recent_avg > earlier_avg + 0.1:
        return "improving"
    else:
        return "stable"


def detect_rumination(
    history: List[BehavioralMemory],
    current: BehavioralMemory,
) -> bool:
    """
    Rumination = repetition + neutral-to-negative sentiment loop.
    """
    recent = last_n(history, 4) + [current]

    repetitive = sum(1 for m in recent if m.repetition_score >= 0.7)
    negative = sum(1 for m in recent if m.sentiment_score <= -0.3)

    return repetitive >= 3 and negative >= 3


def detect_absolutist_escalation(
    history: List[BehavioralMemory],
    current: BehavioralMemory,
) -> bool:
    """
    Tracks increase in absolutist language usage.
    """
    recent = last_n(history, 5)
    past_count = sum(1 for m in recent if m.absolutist_language)

    return current.absolutist_language and past_count >= 2


def assess_risk(
    spiral: bool,
    trend: Optional[str],
    absolutist: bool,
) -> str:
    """
    Conservative safety escalation.
    """
    if spiral and trend == "declining" and absolutist:
        return "medium"

    return "low"


# =================================================
# ORCHESTRATOR
# =================================================

def evaluate_patterns(
    session_history: List[BehavioralMemory],
    current_session: BehavioralMemory,
) -> PatternResult:
    spiral = detect_spiral(session_history, current_session)
    trend = detect_emotional_trend(session_history)
    rumination = detect_rumination(session_history, current_session)
    absolutist = detect_absolutist_escalation(session_history, current_session)
    risk = assess_risk(spiral, trend, absolutist)

    dominant = []
    if spiral:
        dominant.append("repetitive_thought_loop")
    if rumination:
        dominant.append("rumination")
    if absolutist:
        dominant.append("absolutist_language")

    return PatternResult(
        spiral_detected=spiral,
        emotional_trend=trend,
        rumination_detected=rumination,
        absolutist_escalation=absolutist,
        risk_level=risk,
        dominant_signals=dominant,
    )
















