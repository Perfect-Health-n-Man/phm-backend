from app.ai.factory import BaseChatFactory

from .model import Tasks
from ..agent.model import State
from ..chat_dto import ChatDto
from ...firestore import client


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
        if result.decided_tasks:
            doc_ref = client.document("users/" + "testy@example.com")
            await doc_ref.update({"tasks": result.tasks})
            return {"messages": [ChatDto(
                answer=f"{result.answer}\n\n" + "\n".join([f"{str(i + 1)}. {s}" for i, s in enumerate(result.tasks)]),
                form=[])]
            }
        else:
            return {"messages": [ChatDto(answer=result.answer, form=result.form)]}

    def get_tasks(self): ...

    def update_tasks(self): ...

    def delete_tasks(self): ...
