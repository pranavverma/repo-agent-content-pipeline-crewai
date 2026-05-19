import logging
import os
from pathlib import Path

from crewai import Crew, Process
from dotenv import load_dotenv

from src.agents.editor import build_editor
from src.agents.researcher import build_researcher
from src.agents.seo_specialist import build_seo_specialist
from src.agents.writer import build_writer
from src.tasks.content_tasks import editing_task, research_task, seo_task, writing_task

logger = logging.getLogger(__name__)


class ContentCrew:
    """
    Orchestrates four specialised agents in a sequential CrewAI pipeline:

        Researcher → Writer → Editor → SEO Specialist

    Each agent receives the previous agent's output as context automatically
    through CrewAI's sequential process.  The final output is the edited
    article with appended SEO metadata.
    """

    def __init__(self, cfg: dict):
        load_dotenv()
        self._cfg = cfg

        researcher = build_researcher(cfg)
        writer = build_writer(cfg)
        editor = build_editor(cfg)
        seo = build_seo_specialist(cfg)

        tasks = [
            research_task(researcher, topic="{topic}", audience="{audience}"),
            writing_task(writer, topic="{topic}", word_count="{word_count}", tone="{tone}", audience="{audience}"),
            editing_task(editor, tone="{tone}", audience="{audience}"),
            seo_task(seo, topic="{topic}"),
        ]

        self._crew = Crew(
            agents=[researcher, writer, editor, seo],
            tasks=tasks,
            process=Process.sequential,
            verbose=cfg["pipeline"]["verbose"],
        )

    def run(self, topic: str, tone: str, audience: str, word_count: int) -> dict:
        """
        Execute the full pipeline and return a result dict with the article
        content and the output file path.
        """
        logger.info(f"Starting content pipeline — topic: '{topic}'")

        result = self._crew.kickoff(inputs={
            "topic": topic,
            "tone": tone,
            "audience": audience,
            "word_count": word_count,
        })

        # CrewAI returns the last task's output as the crew result
        content = str(result)
        output_path = self._save(topic, content)

        logger.info(f"Pipeline complete — saved to {output_path}")
        return {
            "topic": topic,
            "tone": tone,
            "audience": audience,
            "word_count_target": word_count,
            "content": content,
            "output_file": output_path,
        }

    def _save(self, topic: str, content: str) -> str:
        output_dir = Path(self._cfg["pipeline"]["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        # Sanitise topic for use as a filename
        safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)
        fname = output_dir / f"{safe[:60].strip().replace(' ', '_')}.md"
        fname.write_text(content, encoding="utf-8")
        return str(fname)
