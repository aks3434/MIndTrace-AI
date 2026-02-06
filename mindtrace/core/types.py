from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass(frozen=True)
class Session:
    session_id: str
    started_at: datetime
    ended_at: datetime
    text: str
    confirmed_tags: List[str]
