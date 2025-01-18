from langchain_core.messages import AIMessage
from ai.prompt import get_langchain_prompt
from datetime import datetime
from google.cloud import firestore

from .model import Tasks
from ai.model import get_llm_model_and_callback


class CRUDTasks:
    def __init__(self, doc_ref: firestore.AsyncDocumentReference):
        self.doc_ref = doc_ref

    async def get_user_info(self) -> dict:
        user_ref = await self.doc_ref.get()
        user_info = user_ref.to_dict()["user_info"]
        user_info["datetimeNow"] = datetime.now()
        return user_info

    async def create_tasks(self) -> Tasks:
        get_user_info_task = self.get_user_info()
        langchain_prompt = get_langchain_prompt("createDailyTasks")

        model, langfuse_handler = get_llm_model_and_callback()
        output_parser = Tasks
        chain = langchain_prompt | model.with_structured_output(output_parser)

        user_info = await get_user_info_task
        return await chain.ainvoke(input=user_info, config={"callbacks":[langfuse_handler]})

    def get_tasks(self): ...

    def update_tasks(self): ...

    def delete_tasks(self): ...
