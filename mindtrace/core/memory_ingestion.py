from datetime import datetime
from uuid import UUID

from mindtrace.core.memory_schemas import (
    EpisodicMemory,
    BehavioralMemory,
)


class MemoryIngestor:
    """
    Handles ingestion of raw user input into structured memory.
    """

    def __init__(self, user_id: UUID):
        self.user_id = user_id

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def ingest(self, text: str, session_id: UUID | None = None):
        """
        Ingests a single user input and returns memory objects.
        """
        episodic = self._create_episodic_memory(text, session_id)
        behavioral = self._derive_behavioral_memory(episodic)

        return episodic, behavioral

    # -------------------------------------------------
    # Internal Steps
    # -------------------------------------------------

    def _create_episodic_memory(
        self, text: str, session_id: UUID | None
    ) -> EpisodicMemory:
        """
        Stores raw user input.
        """
        return EpisodicMemory(
            user_id=self.user_id,
            text=text,
            session_id=session_id,
        )

    def _derive_behavioral_memory(
        self, episodic: EpisodicMemory
    ) -> BehavioralMemory:
        """
        Derives simple behavioral signals.
        These are placeholders and will be replaced by ML later.
        """

        text = episodic.text.lower()

        sentiment_score = self._naive_sentiment(text)
        repetition_score = 0.0  # placeholder (embedding later)
        absolutist_language = self._detect_absolutist_language(text)
        time_bucket = self._time_bucket(episodic.timestamp)

        return BehavioralMemory(
            entry_id=episodic.entry_id,
            user_id=episodic.user_id,
            timestamp=episodic.timestamp,
            sentiment_score=sentiment_score,
            repetition_score=repetition_score,
            absolutist_language=absolutist_language,
            time_bucket=time_bucket,
        )

    # -------------------------------------------------
    # Naive Signal Extractors (Temporary)
    # -------------------------------------------------

    def _naive_sentiment(self, text: str) -> float:
        """
        Extremely naive sentiment approximation.
        This exists ONLY to wire the pipeline.
        """
        negative_words = ["bad", "stuck", "tired", "hate", "nothing"]
        positive_words = ["good", "better", "calm", "happy", "progress"]

        score = 0.0
        for w in negative_words:
            if w in text:
                score -= 0.2
        for w in positive_words:
            if w in text:
                score += 0.2

        return max(min(score, 1.0), -1.0)

    def _detect_absolutist_language(self, text: str) -> bool:
        absolutist_terms = ["always", "never", "nothing", "everything"]
        return any(term in text for term in absolutist_terms)

    def _time_bucket(self, timestamp: datetime) -> str:
        hour = timestamp.hour
        if hour < 12:
            return "morning"
        if hour < 18:
            return "evening"
        return "late_night"
