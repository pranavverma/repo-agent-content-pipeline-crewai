import logging
from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ContentRequest, ContentResponse, HealthResponse
from src.crews.content_crew import ContentCrew

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

cfg: dict = {}


def _load_config(path: str = "config/config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cfg
    cfg = _load_config()
    yield


app = FastAPI(
    title="Content Pipeline API",
    description=(
        "Four-agent CrewAI pipeline: Researcher → Writer → Editor → SEO Specialist. "
        "Returns a publication-ready article with SEO metadata for any topic."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", model=cfg.get("openai", {}).get("model", "unknown"))


@app.post("/generate", response_model=ContentResponse)
def generate_content(req: ContentRequest):
    """
    Run the full content pipeline synchronously.

    The pipeline makes multiple LLM calls (one per agent) so response time
    is typically 30-120 seconds depending on topic complexity and word count.
    """
    try:
        crew = ContentCrew(cfg)
        result = crew.run(
            topic=req.topic,
            tone=req.tone,
            audience=req.audience,
            word_count=req.word_count,
        )
    except Exception as exc:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail=str(exc))

    return ContentResponse(**result)
