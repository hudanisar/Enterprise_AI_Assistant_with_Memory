from typing import TypedDict
class AssistantState(TypedDict, total=False):
    user_id: int; conversation_id: int; query: str; chat_history: list; memories: list; retrieved_documents: list; route: str; context: str; response: str; sources: list

