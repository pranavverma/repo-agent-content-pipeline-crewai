from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=5,
        description="The subject the pipeline should research and write about.",
        examples=["The impact of large language models on software development workflows"],
    )
    tone: str = Field(
        default="professional",
        description="Writing tone: professional | conversational | technical",
        pattern="^(professional|conversational|technical)$",
    )
    audience: str = Field(
        default="general",
        description="Target audience: general | technical | executive",
        pattern="^(general|technical|executive)$",
    )
    word_count: int = Field(
        default=800,
        ge=300,
        le=3000,
        description="Target article length in words.",
    )


class ContentResponse(BaseModel):
    topic: str
    tone: str
    audience: str
    word_count_target: int
    content: str
    output_file: str


class HealthResponse(BaseModel):
    status: str
    model: str
