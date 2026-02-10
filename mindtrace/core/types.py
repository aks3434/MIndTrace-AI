from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Session:
    session_id: str
    started_at: datetime
    ended_at: datetime
    text: str
    confirmed_tags: List[str]
