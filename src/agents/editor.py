from crewai import Agent
from langchain_openai import ChatOpenAI


def build_editor(cfg: dict) -> Agent:
    """
    Editor agent — performs a full editorial pass on the Writer's draft.

    Checks for logical consistency, factual alignment with the research brief,
    grammar, clarity, and adherence to the requested tone and audience level.
    Returns the polished article — not a list of suggestions.
    """
    llm = ChatOpenAI(
        model=cfg["openai"]["model"],
        temperature=0.3,  # low temp for precise editorial corrections
    )
    return Agent(
        role="Chief Editor",
        goal=(
            "Review the drafted article for accuracy, clarity, tone, and structure. "
            "Fix grammar, improve awkward phrasing, tighten loose sections, "
            "and ensure the piece flows naturally from intro to conclusion. "
            "Return the final, publication-ready article — not comments."
        ),
        backstory=(
            "You have spent 20 years editing long-form content for top-tier publications. "
            "You have an obsessive eye for detail and a strong sense of narrative structure. "
            "You improve articles without erasing the writer's voice."
        ),
        llm=llm,
        verbose=cfg["pipeline"]["verbose"],
        max_iter=cfg["pipeline"]["max_iterations"],
    )
