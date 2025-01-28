import operator
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class Response(BaseModel):
    answer: str = Field(description="Summary of Answers")
    form: Optional[list[str]] = Field(description="A form to ask questions to users")

class State(BaseModel):
    query: str = Field(..., description="ユーザーからの質問または要望")
    current_agent: str = Field(
        default="4", description="選定されたAIエージェント"
    )
    messages: Annotated[list[Response], operator.add] = Field(
        description="回答履歴"
    )
    current_judge: bool = Field(
        default=False, description="品質チェックの結果"
    )
    judgement_reason: str = Field(
        default="", description="品質チェックの判定理由"
    )

Agent = {
    "1": {
        "name": "タスク作成エージェント",
        "description": "日々のタスクを作成及びデータベースに登録します。",
    },
    "2": {
        "name": "データCRUDエージェント",
        "description": "タスク作成以外のデータCRUDを行います。料理の写真などのdaily logに関連するメッセージであった場合もこのエージェントを選びます。",
    },
    "3": {
        "name": "RAGエージェント",
        "description": "ユーザーからの質問をRAGを利用して回答します。ドキュメントは食物の栄養素や運動、睡眠に関する専門的なデータです。",
    },
    "4": {
        "name": "通常チャットエージェント",
        "description": "会話履歴を読み取りチャットをします。他のエージェントの条件のどれにも当てはまらない場合はこのエージェントを選びます。",
    },
}