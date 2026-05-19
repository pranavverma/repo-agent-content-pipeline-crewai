from crewai import Agent
from langchain_openai import ChatOpenAI


def build_writer(cfg: dict) -> Agent:
    """
    Writer agent — transforms the research brief into a full-length article.

    The temperature is set higher than the Researcher to encourage natural,
    engaging prose rather than bullet-point regurgitation of research notes.
    """
    llm = ChatOpenAI(
        model=cfg["openai"]["model"],
        temperature=cfg["openai"]["temperature"],
    )
    return Agent(
        role="Expert Content Writer",
        goal=(
            "Write a compelling, well-structured article based on the research brief. "
            "Match the requested tone, audience, and word count. "
            "Use clear headings, smooth transitions, and concrete examples."
        ),
        backstory=(
            "You are an award-winning content strategist who has written for major tech "
            "publications. You know how to balance depth with readability and always write "
            "with the target audience in mind. You never plagiarise — all prose is original."
        ),
        llm=llm,
        verbose=cfg["pipeline"]["verbose"],
        max_iter=cfg["pipeline"]["max_iterations"],
    )
