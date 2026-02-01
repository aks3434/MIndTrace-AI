# mindtrace/core/prompt_renderer.py

from pathlib import Path
from typing import Dict

from mindtrace.core.response_planner import ResponsePlan

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


TEMPLATE_MAP = {
    "reflective": "reflective.txt",
    "pattern_reflection": "pattern_reflection.txt",
    "grounding_prompt": "grounding_prompt.txt",
    "gentle_support_suggestion": "support_suggestion.txt",
}


def render_prompt(
    plan: ResponsePlan,
    session_snapshot: Dict,
) -> str:
    """
    Renders a final prompt string based on the response plan
    and session context snapshot.
    """
    if plan.mode not in TEMPLATE_MAP:
        raise ValueError(f"Unknown response mode: {plan.mode}")

    template_path = PROMPT_DIR / TEMPLATE_MAP[plan.mode]

    if not template_path.exists():
        raise FileNotFoundError(
            f"Prompt template not found: {template_path}"
        )

    template = template_path.read_text(encoding="utf-8")

    rendered = (
        template
        .replace("{{SYSTEM_IDENTITY}}", session_snapshot["system_identity"])
        .replace("{{SESSION_CONTEXT}}", _format_session_context(session_snapshot))
    )

    return rendered.strip()

def _format_session_context(snapshot: Dict) -> str:
    """
    Formats session context into a human-readable block
    for prompt injection.
    """
    lines = []

    lines.append(f"- Recent activity: {snapshot['recent_activity']}")
    lines.append(f"- Behavioral trends: {snapshot['behavioral_trends']}")
    lines.append(f"- Active patterns: {snapshot['active_patterns']}")

    if snapshot["risk_flags"]:
        flags = ", ".join(snapshot["risk_flags"])
        lines.append(f"- Risk signals observed: {flags}")

    return "\n".join(lines)