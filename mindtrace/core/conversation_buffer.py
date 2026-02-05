
# mindtrace/core/conversation_buffer.py

class ConversationBuffer:
    """
    Stores verbatim user inputs for the current session only.
    No interpretation. No persistence.
    """

    def __init__(self, max_turns: int = 6):
        self.max_turns = max_turns
        self.turns: list[str] = []

    def add(self, user_input: str):
        self.turns.append(user_input)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)

    def render(self) -> str:
        return "\n".join(f"- {t}" for t in self.turns)