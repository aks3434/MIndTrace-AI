import json
from pathlib import Path
from datetime import datetime
from typing import List
from mindtrace.core.types import Session

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

SESSIONS_FILE = DATA_DIR / "sessions.json"


def load_sessions() -> List[Session]:
    """
    Load all persisted sessions from disk.
    """
    if not SESSIONS_FILE.exists():
        return []

    with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        raw_sessions = json.loads(content)


    sessions: List[Session] = []

    for s in raw_sessions:
        sessions.append(
            Session(
                session_id=s["session_id"],
                started_at=datetime.fromisoformat(s["started_at"]),
                ended_at=datetime.fromisoformat(s["ended_at"]),
                text=s["text"],
                confirmed_tags=s.get("confirmed_tags", []),
            )
        )

    return sessions


def save_session(session: Session) -> None:
    """
    Persist a single session to disk.
    Sessions are append-only.
    """

    sessions = load_sessions()
    sessions.append(session)

    serializable = [
        {
            "session_id": s.session_id,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat(),
            "text": s.text,
            "confirmed_tags": s.confirmed_tags,
        }
        for s in sessions
    ]

    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)

def update_session_tags(session_id: str, tags: list[str]) -> None:
    sessions = load_sessions()

    for s in sessions:
        if s.session_id == session_id:
            s.confirmed_tags = tags
            break

    serializable = [
        {
            "session_id": s.session_id,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat(),
            "text": s.text,
            "confirmed_tags": s.confirmed_tags,
        }
        for s in sessions
    ]

    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)

def update_session_tags_store(session_id: str, tags: list[str]) -> None:
    sessions = load_sessions()

    for s in sessions:
        if s.session_id == session_id:
            s.confirmed_tags = tags
            break

    serializable = [
        {
            "session_id": s.session_id,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat(),
            "text": s.text,
            "confirmed_tags": s.confirmed_tags,
        }
        for s in sessions
    ]

    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)
