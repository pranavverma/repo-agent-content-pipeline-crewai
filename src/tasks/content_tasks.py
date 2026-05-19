from crewai import Agent, Task


def research_task(agent: Agent, topic: str, audience: str) -> Task:
    return Task(
        description=(
            f"Research the following topic thoroughly:\n\n"
            f"Topic: {topic}\n"
            f"Target audience: {audience}\n\n"
            "Deliverable: A structured research brief (markdown) containing:\n"
            "  - Background and context\n"
            "  - Key facts, statistics, and data points with sources\n"
            "  - 3-5 expert perspectives or case studies\n"
            "  - Angles and sub-topics worth covering in the article\n"
            "  - List of credible sources (URLs)"
        ),
        agent=agent,
        expected_output=(
            "A well-organised research brief in markdown format. "
            "All statistics must cite a source URL. "
            "Minimum 400 words."
        ),
    )


def writing_task(agent: Agent, topic: str, word_count: int, tone: str, audience: str) -> Task:
    return Task(
        description=(
            f"Write a full article based on the research brief provided.\n\n"
            f"Topic     : {topic}\n"
            f"Tone      : {tone}\n"
            f"Audience  : {audience}\n"
            f"Word count: approximately {word_count} words\n\n"
            "Structure requirements:\n"
            "  - Engaging headline (H1)\n"
            "  - Introduction with a hook (1-2 paragraphs)\n"
            "  - 3-5 body sections with H2 headings\n"
            "  - Conclusion with a clear takeaway\n"
            "Use concrete examples and avoid filler phrases."
        ),
        agent=agent,
        expected_output=(
            f"A complete article of approximately {word_count} words in markdown format. "
            "No references to the research brief document itself in the article body."
        ),
    )


def editing_task(agent: Agent, tone: str, audience: str) -> Task:
    return Task(
        description=(
            f"Edit the drafted article for publication quality.\n\n"
            f"Expected tone    : {tone}\n"
            f"Target audience  : {audience}\n\n"
            "Checks to perform:\n"
            "  1. Grammar and punctuation\n"
            "  2. Sentence clarity and conciseness (remove padding)\n"
            "  3. Logical flow between sections\n"
            "  4. Tone consistency throughout\n"
            "  5. Factual alignment with the research brief\n"
            "Return the complete revised article — not a list of edits."
        ),
        agent=agent,
        expected_output=(
            "The fully edited, publication-ready article in markdown. "
            "Changes should be integrated — do not annotate the text."
        ),
    )


def seo_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=(
            f"Perform an SEO audit on the edited article about '{topic}' "
            "and produce the final deliverable.\n\n"
            "Required output:\n"
            "  1. The complete edited article (unchanged)\n"
            "  2. A '--- SEO Metadata ---' section appended at the end containing:\n"
            "     - Title tag (≤ 60 chars)\n"
            "     - Meta description (≤ 160 chars)\n"
            "     - Primary keyword\n"
            "     - 5 secondary keywords\n"
            "     - Estimated Flesch readability score (0-100)\n"
            "     - 3 internal-linking suggestions"
        ),
        agent=agent,
        expected_output=(
            "The full article in markdown followed by the '--- SEO Metadata ---' section. "
            "The article body must not be shortened or paraphrased."
        ),
    )
