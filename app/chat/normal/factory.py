from datetime import datetime
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from app.ai.factory import BaseChatFactory
from .model import AiAns


class NormalChatFactory(BaseChatFactory):
    def __init__(self,
                 history: FirestoreChatMessageHistory,
                 user_message: str,
        ) -> None:
        super().__init__(history, "answerQuestions", AiAns, user_message)

    async def create_ans(self) -> AiAns:
        add_human_message_task = self.add_user_message()

        chain = (
            self.prompt
            | self.model.with_structured_output(self.output_parser)
        )

        return await self.add_ai_message(
            chain,
            inputs = {
                "datetimeNow": datetime.now().isoformat(),
                "context": "",
                "chat_history": self.history.messages,
                "question": self.user_message
            },
            add_human_message_task=add_human_message_task
        )