from datetime import datetime , UTC
from typing import List, Dict, Any

from mindtrace.core.boundaries import SYSTEM_IDENTITY
from mindtrace.core.memory_schemas import (
    EpisodicMemory,
    BehavioralMemory,
    CognitivePattern,
)


class SessionContext:
    """
    SessionContext represents MindTrace's internal working memory.

    It is generated BEFORE any response is produced and is never
    shown directly to the user.
    """

    def __init__(
        self,
        recent_episodes: List[EpisodicMemory],
        recent_behavior: List[BehavioralMemory],
        active_patterns: List[CognitivePattern],
    ):
        self.recent_episodes = recent_episodes
        self.recent_behavior = recent_behavior
        self.active_patterns = active_patterns
        self.generated_at = datetime.now(UTC)

    # -------------------------------------------------
    # Public Interface
    # -------------------------------------------------

    def build(self) -> Dict[str, Any]:
        """
        Builds a structured session snapshot.
        This object will later be injected into prompts
        or reasoning layers.
        """
        return {
            "system_identity": SYSTEM_IDENTITY,
            "generated_at": self.generated_at.isoformat(),
            "recent_activity": self._recent_activity_summary(),
            "behavioral_trends": self._behavior_summary(),
            "active_patterns": self._pattern_summary(),
            "risk_flags": self._risk_flags(),
        }

    # -------------------------------------------------
    # Internal Summaries
    # -------------------------------------------------

    def _recent_activity_summary(self) -> str:
        if not self.recent_episodes:
            return "No recent user reflections available."

        return (
            f"{len(self.recent_episodes)} recent reflections recorded. "
            "User is actively expressing thoughts."
        )

    def _behavior_summary(self) -> str:
        if not self.recent_behavior:
            return "Insufficient behavioral data to infer trends."

        avg_sentiment = sum(
            b.sentiment_score for b in self.recent_behavior
        ) / len(self.recent_behavior)

        if avg_sentiment < -0.3:
            trend = "predominantly negative"
        elif avg_sentiment > 0.3:
            trend = "predominantly positive"
        else:
            trend = "emotionally mixed or stable"

        repetition_hits = sum(
            1 for b in self.recent_behavior if b.repetition_score > 0.7
        )

        repetition_note = (
            "Repetitive thought patterns detected."
            if repetition_hits >= 2
            else "No strong repetition detected."
        )

        return f"Emotional trend is {trend}. {repetition_note}"

    def _pattern_summary(self) -> str:
        if not self.active_patterns:
            return "No dominant cognitive patterns currently active."

        pattern_types = sorted({p.pattern_type for p in self.active_patterns})
        return (
            "Active cognitive patterns observed: "
            + ", ".join(pattern_types)
        )

    def _risk_flags(self) -> List[str]:
        """
        Risk flags are NOT diagnoses.
        They simply inform downstream logic to be more cautious.
        """
        flags = []

        negative_entries = [
            b for b in self.recent_behavior if b.sentiment_score < -0.6
        ]
        if len(negative_entries) >= 3:
            flags.append("persistent_negative_emotion")

        repetitive_entries = [
            b for b in self.recent_behavior if b.repetition_score > 0.8
        ]
        if len(repetitive_entries) >= 2:
            flags.append("repetitive_cognition")

        late_night_entries = [
            b for b in self.recent_behavior if b.time_bucket == "late_night"
        ]
        if len(late_night_entries) >= 2:
            flags.append("late_night_vulnerability")

        return flags
