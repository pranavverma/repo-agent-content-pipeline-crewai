import os

from crewai_tools import SerperDevTool, WebsiteSearchTool


def get_search_tools() -> list:
    """
    Return the best available search tools based on what API keys are set.

    SerperDevTool is preferred when SERPER_API_KEY is present (more reliable
    and returns structured results).  Falls back to WebsiteSearchTool which
    uses DuckDuckGo and requires no key.
    """
    if os.getenv("SERPER_API_KEY"):
        return [SerperDevTool()]
    # WebsiteSearchTool with no URL given acts as a general web search
    return [WebsiteSearchTool()]
