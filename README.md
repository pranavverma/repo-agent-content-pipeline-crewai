# Agent Content Pipeline — CrewAI

Provide a topic; four specialised agents collaborate to produce a
publication-ready, SEO-optimised article.  The pipeline runs sequentially:
the Researcher gathers facts and sources, the Writer drafts the article, the
Editor polishes it, and the SEO Specialist appends metadata before saving the
final markdown file.

---

## Pipeline

```
User request (topic + tone + audience + word count)
         │
         ▼
┌───────────────────┐
│    Researcher     │  Searches the web; produces a structured research brief
│ (gpt-4o, T=0.2)  │  with stats, expert views, and source URLs
└────────┬──────────┘
         │ research brief
         ▼
┌───────────────────┐
│      Writer       │  Drafts the full article from the research brief,
│ (gpt-4o, T=0.7)  │  matching the requested tone and word count
└────────┬──────────┘
         │ draft article
         ▼
┌───────────────────┐
│      Editor       │  Fixes grammar, improves clarity, enforces tone
│ (gpt-4o, T=0.3)  │  consistency — returns the final prose
└────────┬──────────┘
         │ edited article
         ▼
┌───────────────────┐
│  SEO Specialist   │  Appends: title tag, meta description, primary +
│ (gpt-4o, T=0.4)  │  secondary keywords, readability score, linking tips
└────────┬──────────┘
         │
    outputs/<topic>.md
```

Each agent receives the previous agent's output via CrewAI's `Process.sequential`.

---

## Technical stack

| Component | Technology |
|-----------|-----------|
| Multi-agent framework | [CrewAI](https://github.com/joaomdmoura/crewAI) |
| LLM | OpenAI GPT-4o (configurable) |
| Web search | Serper API (falls back to DuckDuckGo if no key) |
| API server | FastAPI + Uvicorn |
| Config | YAML + python-dotenv |
| Testing | pytest |

---

## Prerequisites

**OpenAI API key** — required.

```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

Optional — for better web search in the Researcher step:

```bash
# Get a free key at https://serper.dev
SERPER_API_KEY=your_key_here
```

**Python 3.11+**:

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Quick start

### CLI

```bash
python scripts/generate.py "The impact of AI on software testing" \
  --tone professional \
  --audience technical \
  --words 900
```

Expected output:

```
============================================================
  CrewAI Content Pipeline
============================================================
  Topic    : The impact of AI on software testing
  Tone     : professional
  Audience : technical
  Words    : 900
============================================================

[Researcher] Searching for recent statistics on AI in software testing...
[Writer] Drafting article...
[Editor] Reviewing and polishing...
[SEO Specialist] Generating metadata...

============================================================
  Pipeline Complete
============================================================
  Output saved → outputs/The_impact_of_AI_on_software_testing.md

# The Impact of AI on Software Testing

...article content...

--- SEO Metadata ---
Title tag       : How AI Is Transforming Software Testing in 2024
Meta description: Discover how AI-powered tools are reducing testing time...
Primary keyword : AI software testing
Secondary keywords: automated testing AI, machine learning QA, ...
```

### API server

```bash
uvicorn api.main:app --reload
# Docs at http://localhost:8000/docs
```

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The future of quantum computing in cryptography",
    "tone": "technical",
    "audience": "technical",
    "word_count": 1000
  }'
```

---

## API reference

### `POST /generate`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `topic` | string | — | Article topic (required, min 5 chars) |
| `tone` | string | `professional` | `professional` \| `conversational` \| `technical` |
| `audience` | string | `general` | `general` \| `technical` \| `executive` |
| `word_count` | integer | `800` | Target length (300–3000) |

**Response:**

```json
{
  "topic": "...",
  "tone": "professional",
  "audience": "general",
  "word_count_target": 800,
  "content": "# Article Title\n\n...",
  "output_file": "outputs/Article_Title.md"
}
```

### `GET /health`

```json
{ "status": "ok", "model": "gpt-4o" }
```

---

## Configuration — `config/config.yaml`

| Key | Default | Description |
|-----|---------|-------------|
| `openai.model` | `gpt-4o` | Any OpenAI chat model |
| `openai.temperature` | `0.7` | Base temperature (Researcher overrides to 0.2) |
| `pipeline.output_dir` | `outputs` | Directory for saved markdown files |
| `pipeline.max_iterations` | `3` | Per-agent retry budget |
| `pipeline.verbose` | `true` | Log each agent's reasoning steps |
| `content.default_word_count` | `800` | Default word count when omitted from request |

---

## Running tests

```bash
pytest tests/ -v
```

Tests validate agent role definitions, task structures, and goal content
without making any LLM calls.

---

## Project layout

```
├── api/
│   ├── main.py        FastAPI app — /health, /generate
│   └── schemas.py     Pydantic models
├── config/
│   └── config.yaml
├── scripts/
│   └── generate.py    CLI runner
├── src/
│   ├── agents/
│   │   ├── researcher.py     Fact-gathering agent with web search tools
│   │   ├── writer.py         Long-form article drafter
│   │   ├── editor.py         Grammar, clarity, tone reviewer
│   │   └── seo_specialist.py Metadata generator
│   ├── tasks/
│   │   └── content_tasks.py  Task factory functions for each pipeline stage
│   ├── crews/
│   │   └── content_crew.py   ContentCrew — wires agents + tasks, runs pipeline
│   └── tools/
│       └── search_tool.py    Search tool selection (Serper or DuckDuckGo)
└── tests/
    ├── test_agents.py   Agent role/goal/tool construction (offline)
    └── test_crew.py     Task builder validation (offline)
```

---

## Extending this

- **Additional agents** — insert a `FactChecker` agent between Editor and SEO
  Specialist to validate statistics against their source URLs.
- **Different LLMs per agent** — each `build_*` function accepts its own
  `ChatOpenAI` instance; swap in Claude, Mistral, or a local Ollama model per
  agent to optimise cost vs. capability.
- **Async pipeline** — wrap `crew.run()` in a Celery task; return a job ID
  and let the client poll `GET /jobs/{id}` for the finished article.
- **CMS publishing** — after `ContentCrew.run()` returns, POST the markdown
  to WordPress, Contentful, or Ghost via their REST APIs.
