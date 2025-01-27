from pydantic import BaseModel, Field

class Tasks(BaseModel):
    answer: str = Field(description="Summary of Answers")
    form: list[str] = Field(description="The question you want to ask the user or the task they need to complete")