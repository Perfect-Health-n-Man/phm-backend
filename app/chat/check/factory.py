from app.ai.factory import BaseChatFactory
from .model import Judgement
from app.chat.agent.model import State

class CheckFactory(BaseChatFactory):
    def __init__(self) -> None:
        super().__init__("checkAnswer", Judgement)

    async def create_ans(self, state: State) -> dict[str, str | bool]:
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: Judgement = chain.invoke(
            input={
                "chat_history": state.history,
                "question": state.user_message,
                "answer": state.messages[-1].to_str(),
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"current_judge": result.judge, "judgement_reason": result.reason}