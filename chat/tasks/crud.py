from datetime import datetime

import config

from langchain_core.messages import HumanMessage

from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate

langfuse = Langfuse()
langfuse_callback_handler = CallbackHandler()

def create_tasks(user_info):
    langfuse_prompt = langfuse.get_prompt(name="createDailyTasks", label="production")
    langchain_prompt = ChatPromptTemplate(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )
    example_input = {
        "Weight": "60kg",
        "Height": "170cm",
        "Age": "30",
        "DatetimeNow": datetime.now(),
        "Deadline": "今年の3月",
        "Sex": "男",
        "Goal": "55kg",
        "Name": "颯太",
    }

    return langchain_prompt.invoke(input=example_input)

def get_tasks(user_id: str):
    return ""

def update_tasks(): ...

def delete_tasks(): ...

print(create_tasks("a"))
