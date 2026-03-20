import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from .state import AgentState
from .tools import search_news


def fetch_news(state: AgentState) -> AgentState:
    """Fetch news articles using Tavily search."""
    topic = state["topic"]
    articles = search_news(topic)
    return {**state, "articles": articles}


def summarize(state: AgentState) -> AgentState:
    """Summarize the fetched articles using GPT-4o."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    articles = state["articles"]
    topic = state["topic"]

    articles_text = "\n\n".join([
        f"Title: {a['title']}\nURL: {a['url']}\nContent: {a['content']}"
        for a in articles
    ])

    messages = [
        SystemMessage(content=(
            "You are an expert news analyst. Summarize the provided news articles "
            "in a clear, structured format. Include:\n"
            "1. A brief overview (2-3 sentences)\n"
            "2. Key highlights (bullet points)\n"
            "3. Important context or implications\n"
            "Be concise but comprehensive."
        )),
        HumanMessage(content=(
            f"Topic: {topic}\n\nArticles:\n{articles_text}\n\n"
            "Please provide a structured summary of these news articles."
        )),
    ]

    response = llm.invoke(messages)
    return {**state, "summary": response.content, "chat_history": []}


def qa(state: AgentState) -> AgentState:
    """Answer follow-up questions using conversation history and article context."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    articles = state["articles"]
    summary = state["summary"]
    question = state["question"]
    chat_history = state.get("chat_history", [])

    articles_text = "\n\n".join([
        f"Title: {a['title']}\nURL: {a['url']}\nContent: {a['content']}"
        for a in articles
    ])

    messages = [
        SystemMessage(content=(
            f"You are a helpful assistant answering questions about news articles.\n\n"
            f"Context - News Summary:\n{summary}\n\n"
            f"Context - Full Articles:\n{articles_text}\n\n"
            "Answer questions based on this context. Be accurate and cite sources when relevant."
        )),
    ]

    # Add chat history
    for entry in chat_history:
        if entry["role"] == "user":
            messages.append(HumanMessage(content=entry["content"]))
        elif entry["role"] == "assistant":
            messages.append(AIMessage(content=entry["content"]))

    messages.append(HumanMessage(content=question))

    response = llm.invoke(messages)
    answer = response.content

    # Update chat history
    updated_history = chat_history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]

    return {**state, "answer": answer, "chat_history": updated_history}
