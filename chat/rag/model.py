from pydantic import BaseModel, Field

class AiRagAns(BaseModel):
    cot: str = Field(description="COT thought process")
    summary: str = Field(description="Summary of Answers")
