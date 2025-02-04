from app.ai.factory import BaseChatFactory

from .model import Tasks
from ..agent.model import State
from ..chat_dto import ChatDto


class TasksFactory(BaseChatFactory):
    def __init__(self, session_id: str) -> None:
        super().__init__("createDailyTasks", Tasks, session_id)

    async def create_tasks(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: Tasks = chain.invoke(
            input={
                "user_message": state.user_message,
                "history": state.history,
                "user_info": state.user_info,
                "datetimeNow": state.datetimeNow,
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}

    def get_tasks(self): ...

    def update_tasks(self): ...

    def delete_tasks(self): ...
