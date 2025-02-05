import json
from datetime import datetime

from app.ai.factory import BaseChatFactory
from .model import AiAns
from ..agent.model import State
from ..chat_dto import ChatDto
from app.firestore import client


class NormalChatFactory(BaseChatFactory):
    def __init__(self, session_id: str) -> None:
        super().__init__("answerQuestions", AiAns, session_id)

    async def create_ans(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
            self.prompt
            | self.model.with_structured_output(self.output_parser)
        )
        today = datetime.now().strftime('%Y-%m-%d')
        doc_ref = await client.document("users", state.user_id, "daily_logs", today).get()
        daily_logs = doc_ref.to_dict()
        result: AiAns = await chain.ainvoke(
            input={
                "datetimeNow": state.datetimeNow,
                "context": "",
                "chat_history": state.history,
                "user_message": state.user_message,
                "user_info": state.user_info,
                "tasks": state.tasks,
                "daily_logs": json.dumps(daily_logs, indent=2),
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}
