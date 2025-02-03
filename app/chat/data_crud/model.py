from pydantic import BaseModel, Field

class ChoosePath(BaseModel):
    filepaths: list[str] = Field(description="List of file paths to choose")

class CRUDTask(BaseModel):
    answer: str = Field(description="Summary of Answers")
    form: list[str] = Field(
        default_factory=list,
        description="The question you want to ask the user if there are two or more"
    )

crud_diagram = """
/users (コレクション)
├── {userId} (ドキュメント)
    ├── user_info: map
        ├── name: string [C, R, U]
        ├── birthday: string [C, R]
        ├── gender: string [C, R]
        ├── goals: array(string) [C, R, U]]
    ├── daily_logs (サブコレクション)
        ├── {dateId} (ドキュメント: YYYY-MM-DD形式)
            ├── diary: string [C, R, U]
            ├── meals: map [C, R, U]
            ├── sleep: map [C, R, U]
            ├── exercises: map [C, R, U]
"""