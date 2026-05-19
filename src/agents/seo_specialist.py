from crewai import Agent
from langchain_openai import ChatOpenAI


def build_seo_specialist(cfg: dict) -> Agent:
    """
    SEO Specialist agent — adds metadata and inline optimisations after editing.

    Produces the final deliverable: the article with an SEO title, meta
    description, primary/secondary keyword suggestions, and readability score.
    Does NOT rewrite content — only augments it with SEO metadata.
    """
    llm = ChatOpenAI(
        model=cfg["openai"]["model"],
        temperature=0.4,
    )
    return Agent(
        role="SEO Specialist",
        goal=(
            "Analyse the edited article and produce an SEO report including:\n"
            "  1. Optimised title tag (≤ 60 characters)\n"
            "  2. Meta description (≤ 160 characters)\n"
            "  3. Primary keyword and 5 secondary keywords\n"
            "  4. Estimated Flesch readability score and recommended target\n"
            "  5. 3 internal-linking opportunities (section headings that pair well)\n"
            "Then return the full article with the SEO metadata appended as a "
            '"--- SEO Metadata ---" section at the bottom.'
        ),
        backstory=(
            "You are an SEO strategist with 12 years of experience helping content rank "
            "on page one. You understand search intent, keyword density, and on-page "
            "signals without keyword-stuffing. You always preserve readability."
        ),
        llm=llm,
        verbose=cfg["pipeline"]["verbose"],
        max_iter=cfg["pipeline"]["max_iterations"],
    )
