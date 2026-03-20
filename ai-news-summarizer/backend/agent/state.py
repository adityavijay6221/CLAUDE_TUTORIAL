from typing import TypedDict, Optional


class AgentState(TypedDict):
    topic: str
    articles: list[dict]       # Raw Tavily results
    summary: str               # GPT-4o generated summary
    chat_history: list         # Conversation memory for Q&A
    question: Optional[str]    # Follow-up question (optional)
    answer: Optional[str]      # Q&A answer (optional)
