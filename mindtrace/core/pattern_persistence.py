from datetime import datetime , UTC
from typing import List 
from mindtrace.core.memory_schemas import CognitivePattern
from mindtrace.core.patterns import PatternResult

def persist_cognitive_patterns(
    user_id,
    pattern_result: PatternResult,
    existing_patterns: List[CognitivePattern],
) -> List[CognitivePattern]:
    """
    Converts PatternResult into long-term CognitivePattern memory.
    """
    now = datetime.now(UTC)
    updated_patterns = existing_patterns.copy()

    def upsert(pattern_type: str, description: str):
        for p in updated_patterns:
            if p.pattern_type == pattern_type:
                p.last_detected = now
                p.recurrence_level = pattern_result.risk_level
                return

        updated_patterns.append(
            CognitivePattern(
                user_id=user_id,
                pattern_type=pattern_type,
                description=description,
                recurrence_level=pattern_result.risk_level,
                first_detected=now,
                last_detected=now,
            )
        )

    if pattern_result.spiral_detected:
        upsert(
            "spiral",
            "Sustained repetitive cognitive patterns detected over time.",
        )

    if pattern_result.rumination_detected:
        upsert(
            "rumination",
            "Repetitive negative thought loops with low emotional resolution.",
        )

    return updated_patterns