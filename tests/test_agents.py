"""
Unit tests for agent construction.
Validates roles, goals, and config wiring — no LLM calls made.
"""

import pytest

BASE_CFG = {
    "openai": {"model": "gpt-4o", "temperature": 0.7},
    "pipeline": {"verbose": False, "max_iterations": 2, "output_dir": "/tmp/test_outputs"},
    "content": {"default_word_count": 800, "default_tone": "professional", "default_audience": "general"},
}


class TestResearcherAgent:
    def test_role(self):
        from src.agents.researcher import build_researcher
        a = build_researcher(BASE_CFG)
        assert "Research" in a.role

    def test_has_tools(self):
        from src.agents.researcher import build_researcher
        a = build_researcher(BASE_CFG)
        assert len(a.tools) > 0


class TestWriterAgent:
    def test_role(self):
        from src.agents.writer import build_writer
        a = build_writer(BASE_CFG)
        assert "Writer" in a.role

    def test_no_tools_needed(self):
        # Writer works from context — it should not need external search tools
        from src.agents.writer import build_writer
        a = build_writer(BASE_CFG)
        assert a.tools is None or len(a.tools) == 0


class TestEditorAgent:
    def test_role(self):
        from src.agents.editor import build_editor
        a = build_editor(BASE_CFG)
        assert "Editor" in a.role

    def test_goal_mentions_publication_ready(self):
        from src.agents.editor import build_editor
        a = build_editor(BASE_CFG)
        assert "publication" in a.goal.lower() or "return" in a.goal.lower()


class TestSEOAgent:
    def test_role(self):
        from src.agents.seo_specialist import build_seo_specialist
        a = build_seo_specialist(BASE_CFG)
        assert "SEO" in a.role

    def test_goal_mentions_metadata(self):
        from src.agents.seo_specialist import build_seo_specialist
        a = build_seo_specialist(BASE_CFG)
        assert "meta" in a.goal.lower()
