"""
Structural tests for the ContentCrew pipeline.
Verifies task definitions and crew composition without making LLM calls.
"""

import pytest
from crewai import Task

from src.tasks.content_tasks import editing_task, research_task, seo_task, writing_task


BASE_CFG = {
    "openai": {"model": "gpt-4o", "temperature": 0.7},
    "pipeline": {"verbose": False, "max_iterations": 2, "output_dir": "/tmp"},
    "content": {"default_word_count": 800, "default_tone": "professional", "default_audience": "general"},
}


class TestTaskBuilders:
    def _dummy_agent(self):
        from unittest.mock import MagicMock
        return MagicMock()

    def test_research_task_is_task_instance(self):
        t = research_task(self._dummy_agent(), topic="AI trends", audience="general")
        assert isinstance(t, Task)

    def test_research_task_description_contains_topic(self):
        t = research_task(self._dummy_agent(), topic="blockchain scalability", audience="technical")
        assert "blockchain scalability" in t.description

    def test_writing_task_includes_word_count(self):
        t = writing_task(self._dummy_agent(), topic="test", word_count=1200, tone="conversational", audience="general")
        assert "1200" in t.description

    def test_editing_task_expected_output_mentions_article(self):
        t = editing_task(self._dummy_agent(), tone="professional", audience="executive")
        assert "article" in t.expected_output.lower()

    def test_seo_task_mentions_metadata(self):
        t = seo_task(self._dummy_agent(), topic="cloud computing")
        assert "SEO Metadata" in t.description
