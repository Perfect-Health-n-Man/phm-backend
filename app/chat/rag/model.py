from pydantic import BaseModel, Field

class AiRagAns(BaseModel):
    cot: str = Field(description="COT thought process")
    rag: str = Field(description="Documents referenced as RAG")
    answer: str = Field(description="Summary of Answers")
