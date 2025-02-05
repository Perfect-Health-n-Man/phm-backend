from pydantic import BaseModel, Field

class Tasks(BaseModel):
    # cot: str = Field(description="COT thought process")
    answer: str = Field(description="Summary of AI Answer")
    form: list[str] = Field(
        default_factory=list,
        description="The question form you want to ask the user"
    )
    decided_tasks: bool = Field(
        default=False,
        description="タスクが決定したかどうか。"
    )
    tasks: list[str] = Field(
        default_factory=list,
        description="決定したタスク。タスクが決定した場合のみ記入する。"
    )