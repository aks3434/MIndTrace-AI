from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# =================================================
# 1. USER PROFILE MEMORY (STATIC CONTEXT)
# =================================================

class UserProfile(BaseModel):
    """
    Static user context.
    This is NOT analyzed emotionally.
    """

    user_id: UUID = Field(default_factory=uuid4)
    age_range: Optional[str] = Field(
        None, description="e.g. '18-24', '25-30'"
    )
    gender: Optional[str] = Field(
        None, description="User-identified gender"
    )
    timezone: str = "UTC"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# =================================================
# 2. EPISODIC MEMORY (RAW USER INPUT)
# =================================================

class EpisodicMemory(BaseModel):
    """
    Raw, immutable user input.
    This is the source of truth.
    """

    entry_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    text: str
    user_tags: Optional[List[str]] = []
    session_id: Optional[UUID] = None


# =================================================
# 3. BEHAVIORAL MEMORY (DERIVED SIGNALS)
# =================================================

class BehavioralMemory(BaseModel):
    """
    Computed signals from episodic memory.
    These are descriptive, not diagnostic.
    """

    entry_id: UUID
    user_id: UUID
    timestamp: datetime

    sentiment_score: float = Field(
        ..., description="Range: -1 (negative) to +1 (positive)"
    )
    repetition_score: float = Field(
        ..., description="Semantic repetition intensity (0–1)"
    )
    absolutist_language: bool = False
    time_bucket: Optional[str] = Field(
        None, description="morning | evening | late_night"
    )


# =================================================
# 4. COGNITIVE PATTERN MEMORY (LONG-TERM)
# =================================================

class CognitivePattern(BaseModel):
    """
    High-level recurring patterns detected over time.
    """

    pattern_id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    pattern_type: str = Field(
        ..., description="spiral | rumination | avoidance | growth"
    )
    description: str

    trigger_context: Optional[str] = None
    recurrence_level: str = Field(
        ..., description="low | medium | high"
    )

    first_detected: datetime
    last_detected: datetime
