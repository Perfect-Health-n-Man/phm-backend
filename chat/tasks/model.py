from pydantic import BaseModel, Field

class Tasks(BaseModel):
    tasks: list[str] = Field(description="Common tasks that users should perform")