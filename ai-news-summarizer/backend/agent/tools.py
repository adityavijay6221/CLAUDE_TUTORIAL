import os
from tavily import TavilyClient


def search_news(topic: str, max_results: int = 5) -> list[dict]:
    """Search for news articles using Tavily API."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(
        query=topic,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False,
    )
    articles = []
    for result in response.get("results", []):
        articles.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "published_date": result.get("published_date", ""),
        })
    return articles
