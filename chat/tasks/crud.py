from ai.model import get_llm_model_and_callback
from ai.prompt import get_prompt
from firestore.crud import get_user

from langchain_core.output_parsers import StrOutputParser
from datetime import datetime
from google.cloud import firestore
from langfuse import Langfuse

async def get_user_info(fs_aclient: firestore.AsyncClient, user_id: str) -> dict:
    doc_ref = get_user(fs_aclient, user_id)
    user_ref = await doc_ref.get()
    user_info = user_ref.to_dict()["user_info"]
    user_info["datetimeNow"] = datetime.now()
    return user_info

async def create_tasks(fs_aclient: firestore.AsyncClient, lf_client: Langfuse, user_id: str) -> str:
    get_user_info_task = get_user_info(fs_aclient, user_id)
    langchain_prompt = get_prompt(lf_client, "createDailyTasks")

    model, langfuse_handler = get_llm_model_and_callback()
    output_parser = StrOutputParser()
    chain = langchain_prompt | model | output_parser

    user_info = await get_user_info_task
    return await chain.ainvoke(input=user_info, config={"callbacks":[langfuse_handler]})

def get_tasks(): ...

def update_tasks(): ...

def delete_tasks(): ...
