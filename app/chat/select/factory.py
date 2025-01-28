from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from app.ai.factory import BaseChatFactory
from app.chat.select.model import SelectAgent, model


class SelectAgentFactory(BaseChatFactory):
    def __init__(self,
                 history: FirestoreChatMessageHistory,
                 user_message: str,
                 ) -> None:
        super().__init__(history, "selectAgent", SelectAgent, user_message)
        self.model = model

    async def create_ans(self) -> SelectAgent:
        add_human_message_task = self.add_user_message()

        chain = (
            self.prompt
            | self.model.with_structured_output(self.output_parser)
        )

        return await self.add_ai_message(
            chain,
            inputs = {
                "chat_history": self.history.messages[-10:],
                "question": self.user_message
            },
            add_human_message_task=add_human_message_task
        )