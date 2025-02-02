from pydantic import BaseModel, Field

class AiAns(BaseModel):
    cot: str = Field(description="COT thought process")
    answer: str = Field(description="Summary of Answers")
    form: list[str] = Field(
        default_factory=list,
        description="The question you want to ask the user if there are two or more"
    )
