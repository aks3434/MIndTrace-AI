from dataclasses import dataclass


@dataclass
class ResponsePlan:
    """
    Describes HOW MindTrace is allowed to respond.
    The LLM must never violate this contract.
    """
    mode: str  # reflective | pattern_reflection | grounding_prompt | gentle_support_suggestion
    allow_questions: bool
    allow_suggestions: bool
    include_support_note: bool

from mindtrace.core.boundaries import should_escalate
from mindtrace.core.session_context import SessionContext
from mindtrace.core.response_planner import ResponsePlan  

def plan_response(ctx: SessionContext) -> ResponsePlan:
    """
    Determines the allowed response mode based on session context.
    """
    snapshot = ctx.build()

    active_patterns = snapshot["active_patterns"]
    risk_flags = snapshot["risk_flags"]

    # --- Escalation path (highest priority) ---
    if should_escalate(
        risk_level="low",  # planner does NOT decide risk
        risk_flags=risk_flags,
    ):
        return ResponsePlan(
            mode="gentle_support_suggestion",
            allow_questions=False,
            allow_suggestions=True,
            include_support_note=True,
        )

    # --- Rumination → grounding ---
    if "rumination" in active_patterns:
        return ResponsePlan(
            mode="grounding_prompt",
            allow_questions=False,
            allow_suggestions=False,
            include_support_note=False,
        )

    # --- Pattern reflection ---
    if active_patterns and "No dominant" not in active_patterns:
        return ResponsePlan(
            mode="pattern_reflection",
            allow_questions=True,
            allow_suggestions=False,
            include_support_note=False,
        )

    # --- Default: neutral reflection ---
    return ResponsePlan(
        mode="reflective",
        allow_questions=True,
        allow_suggestions=False,
        include_support_note=False,
    )

