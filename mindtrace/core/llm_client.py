# core/llm_client.py
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

GREETING_RESPONSES = [
    "Hi — welcome to MindTrace. You can share whatever’s been on your mind.",
    "Hey. This is MindTrace. Take your time — you can start wherever you want.",
    "Hello. MindTrace is ready when you are."
]
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
)



SYSTEM_PROMPT = """
You are MindTrace, a reflective system that renders observations
derived from verified user-authored records.

Rules:
- Do NOT use absolute or definitive language (e.g., "this means", "you are").
- Do NOT introduce new interpretations.
- Do NOT diagnose or label mental states.
- Do NOT speculate beyond provided data.
- Do NOT give advice unless explicitly instructed.
- Use calm, grounded, non-authoritative language.
- Frame outputs as observations, not conclusions.
"""

def render_response(payload: dict) -> str:
    """
    payload is a fully-formed, verified structure produced by the system.
    The LLM must only render it into natural language.
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=format_payload(payload)),
    ]

    response = llm.invoke(messages)
    return response.content.strip()


def format_payload(payload) -> str:
    """
    Convert structured observations into a neutral, descriptive
    rendering prompt. Deterministic and non-interpretive.
    """

    markers_block = ""
    if getattr(payload, "descriptive_markers", None):
        
        markers_block = "\nObserved characteristics:\n" + "\n".join(
            f"- {m}" for m in payload.descriptive_markers
        )

    return f"""
Verified observations:
- Topic: {payload.topic}
- Sessions analyzed: {payload.session_count}
- Time span: {payload.time_range}
- Confidence: {payload.confidence}

Evidence summary:
{payload.evidence_summary}
{markers_block}

Instructions:
- Describe how the above pattern appears across sessions.
- You may elaborate descriptively on the observed characteristics.
- Do NOT explain causes, assign meaning, or label mental states.
- Do NOT give advice or recommendations.
- Frame the response as an observation, not a conclusion.
"""

_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4)

_REFLECTION_SYSTEM_PROMPT = """
You are MindTrace.
You respond with calm, reflective language.

Rules:
- Do NOT analyze patterns
- Do NOT diagnose or label
- Do NOT give advice unless explicitly asked
- Do NOT reference mental health conditions
- Reflect the user's words gently and neutrally
- Keep responses concise and grounded
"""


def render_reflection(text: str) -> str:
    messages = [
        SystemMessage(content=_REFLECTION_SYSTEM_PROMPT),
        HumanMessage(content=text),
    ]
    return _llm.invoke(messages).content.strip()
