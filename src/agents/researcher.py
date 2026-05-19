from crewai import Agent
from langchain_openai import ChatOpenAI

from src.tools.search_tool import get_search_tools


def build_researcher(cfg: dict) -> Agent:
    """
    Researcher agent — gathers factual information, statistics, and sources
    on the given topic before the Writer begins drafting.

    Uses a lower temperature than the other agents because factual accuracy
    matters more than creativity at this stage.
    """
    llm = ChatOpenAI(
        model=cfg["openai"]["model"],
        temperature=0.2,  # deliberate override — factual retrieval, not creativity
    )
    return Agent(
        role="Senior Research Analyst",
        goal=(
            "Conduct thorough research on the given topic. "
            "Find recent statistics, expert opinions, real-world examples, and credible sources. "
            "Produce a structured research brief that the Writer can use as a foundation."
        ),
        backstory=(
            "You are a meticulous researcher with 15 years of experience across technology, "
            "business, and science journalism. You never fabricate facts — if you cannot find "
            "a credible source, you say so explicitly."
        ),
        tools=get_search_tools(),
        llm=llm,
        verbose=cfg["pipeline"]["verbose"],
        max_iter=cfg["pipeline"]["max_iterations"],
    )
