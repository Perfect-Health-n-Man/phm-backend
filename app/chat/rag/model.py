from typing import Optional

from pydantic import BaseModel, Field

class AiRagAns(BaseModel):
    cot: str = Field(description="COT thought process")
    rag: str = Field(description="Documents referenced as RAG")
    answer: str = Field(description="Summary of Answers")
    form: list[str] = Field(
        default_factory=list,
        description="The question you want to ask the user if there are two or more"
    )
