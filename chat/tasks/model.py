from pydantic import BaseModel, Field

class questionForTasks(BaseModel):
    question: list[str] = Field(description="The questions to ask the user to create the task")

class Tasks(BaseModel):
    tasks: list[str] = Field(description="Common tasks that users should perform")