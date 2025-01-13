import config
from ai.model import get_llm_model_and_callback
from ai.prompt import get_prompt

from langchain_core.output_parsers import StrOutputParser
from datetime import datetime
from google.cloud import firestore

def get_user_info(db: firestore.Client, user_id: str) -> dict:
    user_ref = db.collection("users").document(user_id).get()
    user_info = user_ref.to_dict()["user_info"]
    user_info["datetimeNow"] = datetime.now()
    return user_info



def create_tasks(db: firestore.Client, user_id: str) -> str:
    user_info = get_user_info(db, user_id)

    langchain_prompt = get_prompt("createDailyTasks")

    model, langfuse_handler = get_llm_model_and_callback()
    output_parser = StrOutputParser()
    chain = langchain_prompt | model | output_parser

    return chain.invoke(input=user_info, config={"callbacks":[langfuse_handler]})

def get_tasks(): ...

def update_tasks(): ...

def delete_tasks(): ...

db = firestore.Client()
print(create_tasks(db, "user-id"))
