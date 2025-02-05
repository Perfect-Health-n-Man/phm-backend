import operator
from typing import Annotated

from pydantic import BaseModel, Field

from app.chat.chat_dto import ChatDto


class State(BaseModel):
    user_message: str = Field(..., description="ユーザーからの質問または要望")
    history: str = Field(..., description="チャット履歴")
    datetimeNow: str = Field(..., description="現在日時")
    user_id: str = Field(..., description="ユーザーID")
    tasks: str = Field(..., description="日々のタスク")
    user_info: str = Field(..., description="ユーザー情報")
    current_agent: int = Field(
        default=4,
        description="選定されたAIエージェント"
    )
    messages: Annotated[list[ChatDto], operator.add] = Field(
        default_factory=list,
        description="回答履歴"
    )
    current_judge: bool = Field(
        default=False,
        description="品質チェックの結果"
    )
    judgement_reason: str = Field(
        default="",
        description="品質チェックの判定理由"
    )
    session_id: str = Field(description="Langfuse 用 session ID")
    loop: int = Field(
        default=0,
        description="通らなかったチェックの回数"
    )
    model_config = {
        "arbitrary_types_allowed": True
    }

def to_ai_response(state: State) -> ChatDto:
    return state["messages"][-1]

Agent = {
    "1": {
        "name": "タスク作成エージェント",
        "description": "日々のタスクを作成及びデータベースに登録します。日々のタスクが存在しない場合は必ずこの選択肢を選びます。",
    },
    "2": {
        "name": "データCRUDエージェント",
        "description": "タスク作成以外のデータCRUDを行います。料理の写真などのdaily logsに関連するメッセージであった場合もこのエージェントを選びます。",
    },
    "3": {
        "name": "RAGエージェント",
        "description": "ユーザーからの質問をRAGを利用して回答します。ドキュメントは食物の栄養素や運動、睡眠に関する専門的なデータです。",
    },
    "4": {
        "name": "通常チャットエージェント",
        "description": "普通のチャットをします。他のエージェントの条件のどれにも当てはまらない場合はこのエージェントを選びます。",
    },
}