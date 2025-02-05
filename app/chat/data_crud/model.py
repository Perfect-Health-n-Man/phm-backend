from pydantic import BaseModel, Field

class CRUDTask(BaseModel):
    answer: str = Field(description="Summary of AI Answer")
    operation: str = Field(
        default="NOT_ALLOWED",
        description="The operation you want to perform on the selected file"
    )
    document_path: str = Field(
        # default="",
        description="the document path"
    )
    data_path: list[str] = Field(
        # default_factory=list,
        description="the data path. 例）['meals', 'meals1', 'calories']"
    )
    contents: str = Field(
        default="",
        description="Contents of data"
    )