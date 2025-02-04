from app.ai.factory import BaseChatFactory
from .model import ChoosePath, CRUDTask, crud_diagram
from ..agent.model import State
from ..chat_dto import ChatDto


class ChoosePathFactory(BaseChatFactory):
    def __init__(self) -> None:
        super().__init__("choosePath", ChoosePath)

    async def choose_path(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: ChoosePath = await chain.ainvoke(
            input={
                "datetimeNow": state.datetimeNow,
                "chat_history": state.history,
                "question": state.user_message,
                "crud_diagram": crud_diagram,
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}
