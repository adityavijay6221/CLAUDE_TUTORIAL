from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import fetch_news, summarize, qa


def build_summarize_graph() -> StateGraph:
    """Build the LangGraph for news summarization."""
    graph = StateGraph(AgentState)

    graph.add_node("fetch_news", fetch_news)
    graph.add_node("summarize", summarize)

    graph.set_entry_point("fetch_news")
    graph.add_edge("fetch_news", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


def build_qa_graph() -> StateGraph:
    """Build the LangGraph for Q&A follow-up."""
    graph = StateGraph(AgentState)

    graph.add_node("qa", qa)

    graph.set_entry_point("qa")
    graph.add_edge("qa", END)

    return graph.compile()


summarize_graph = build_summarize_graph()
qa_graph = build_qa_graph()
