from langchain_core.messages import AIMessage

from ai.model import get_llm_model_and_callback
from ai.prompt import get_langchain_prompt
from firestore.firestore_crud import get_user

from langchain_core.output_parsers import StrOutputParser
from datetime import datetime
from google.cloud import firestore
from langfuse import Langfuse

async def get_user_info(doc_ref: firestore.AsyncDocumentReference) -> dict:
    user_ref = await doc_ref.get()
    user_info = user_ref.to_dict()["user_info"]
    user_info["datetimeNow"] = datetime.now()
    return user_info

async def create_tasks(doc_ref: firestore.AsyncDocumentReference, lf_client: Langfuse) -> AIMessage:
    get_user_info_task = get_user_info(doc_ref)
    langchain_prompt = get_langchain_prompt("createDailyTasks")

    model, langfuse_handler = get_llm_model_and_callback()
    output_parser = StrOutputParser()
    chain = langchain_prompt | model | output_parser

    user_info = await get_user_info_task
    content = await chain.ainvoke(input=user_info, config={"callbacks":[langfuse_handler]})
    return AIMessage(content=content)

def get_tasks(): ...

def update_tasks(): ...

def delete_tasks(): ...
