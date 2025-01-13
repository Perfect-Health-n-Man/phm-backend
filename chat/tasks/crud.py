import config
from ai.model import get_llm_model_and_callback

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langfuse import Langfuse
from datetime import datetime
from google.cloud import firestore

langfuse = Langfuse()

def create_tasks(user_info):
    langfuse_prompt = langfuse.get_prompt(name="createDailyTasks", label="production")
    langchain_prompt = ChatPromptTemplate(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )

    model, langfuse_handler = get_llm_model_and_callback()
    output_parser = StrOutputParser()
    chain = langchain_prompt | model |output_parser

    user_info["datetimeNow"] = datetime.now()

    return chain.invoke(input=user_info, config={"callbacks":[langfuse_handler]})

def get_tasks(user_id: str):
    return ""

def update_tasks(): ...

def delete_tasks(): ...

db = firestore.Client()
user_ref = db.collection("users").document('user-id').get()
user_info = user_ref.to_dict()["user_info"]
print(create_tasks(user_info))
