import config

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langfuse import Langfuse
from datetime import datetime

from ai.model import get_llm_model_and_callback

langfuse = Langfuse()

def create_tasks(user_info):
    langfuse_prompt = langfuse.get_prompt(name="createDailyTasks", label="production")
    langchain_prompt = ChatPromptTemplate(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )

    model, langfuse_handler = get_llm_model_and_callback()
    chain = langchain_prompt | model | StrOutputParser()

    example_input = {
        "Weight": "70kg",
        "Height": "170cm",
        "Age": "26",
        "DatetimeNow": datetime.now(),
        "Deadline": "今年の3月",
        "Sex": "男",
        "Goal": "65kg",
        "Name": "颯太",
    }

    return chain.invoke(input=example_input, config={"callbacks":[langfuse_handler]})

def get_tasks(user_id: str):
    return ""

def update_tasks(): ...

def delete_tasks(): ...

print(create_tasks("a"))
