from app.ai.factory import BaseChatFactory
from datetime import datetime
from google.cloud.firestore import AsyncClient

from .model import Tasks
from ..agent.model import State
from ..chat_dto import ChatDto


class TasksFactory(BaseChatFactory):
    def __init__(self,
                 fs_aclient: AsyncClient,
                 user_id: str,
                 session_id: str,
                 ) -> None:
        super().__init__("createDailyTasks", Tasks, session_id)
        self.fs_aclient = fs_aclient
        self.user_id = user_id

    async def get_user_info(self, state: State) -> dict:
        user_ref = await self.fs_aclient.document("users", self.user_id).get()
        user_info = user_ref.to_dict()["user_info"]
        user_info["datetimeNow"] = datetime.now()
        user_info["user_message"] = state.user_message
        user_info["history"] = state.history
        return user_info

    async def create_tasks(self, state: State) -> dict[str, list[ChatDto]]:
        get_user_info_task = self.get_user_info(state)
        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        user_info = await get_user_info_task
        result: Tasks = chain.invoke(
            input=user_info,
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}

    def get_tasks(self): ...

    def update_tasks(self): ...

    def delete_tasks(self): ...
