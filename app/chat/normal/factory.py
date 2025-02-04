from app.ai.factory import BaseChatFactory
from .model import AiAns
from ..agent.model import State
from ..chat_dto import ChatDto


class NormalChatFactory(BaseChatFactory):
    def __init__(self, session_id: str) -> None:
        super().__init__("answerQuestions", AiAns, session_id)

    async def create_ans(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
            self.prompt
            | self.model.with_structured_output(self.output_parser)
        )
        result: AiAns = await chain.ainvoke(
            input={
                "datetimeNow": state.datetimeNow,
                "context": "",
                "chat_history": state.history,
                "user_message": state.user_message,
                "user_info": state.user_info,
                "tasks": state.tasks,
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}
