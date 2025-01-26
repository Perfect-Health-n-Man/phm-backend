from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from ai.factory import BaseChatFactory
from datetime import datetime
from google.cloud import firestore

from .model import Tasks


class TasksFactory(BaseChatFactory):
    def __init__(self,
                 doc_ref: firestore.AsyncDocumentReference,
                 history: FirestoreChatMessageHistory,
                 ) -> None:
        super().__init__(history, "createDailyTasks", Tasks, "タスクを考えて")
        self.doc_ref = doc_ref

    async def get_user_info(self) -> dict:
        user_ref = await self.doc_ref.get()
        user_info = user_ref.to_dict()["user_info"]
        user_info["datetimeNow"] = datetime.now()
        return user_info

    async def create_tasks(self) -> Tasks:
        get_user_info_task = self.get_user_info()
        add_human_message_task = self.add_user_message()

        chain = (
                self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        user_info = await get_user_info_task
        return await self.add_ai_message(
            chain,
            inputs=user_info,
            add_human_message_task=add_human_message_task
        )

    def get_tasks(self): ...

    def update_tasks(self): ...

    def delete_tasks(self): ...
