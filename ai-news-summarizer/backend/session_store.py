import uuid
from typing import Optional
from .agent.state import AgentState


# In-memory session store: maps session_id -> AgentState
_sessions: dict[str, AgentState] = {}


def create_session(state: AgentState) -> str:
    """Create a new session and return its ID."""
    session_id = str(uuid.uuid4())
    _sessions[session_id] = state
    return session_id


def get_session(session_id: str) -> Optional[AgentState]:
    """Retrieve session state by ID."""
    return _sessions.get(session_id)


def update_session(session_id: str, state: AgentState) -> None:
    """Update existing session state."""
    _sessions[session_id] = state


def delete_session(session_id: str) -> None:
    """Delete a session."""
    _sessions.pop(session_id, None)
