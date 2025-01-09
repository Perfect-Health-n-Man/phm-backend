import config

from langchain_core.messages import HumanMessage

from langfuse.prompt import get_prompt

def create_tasks(user_info):
    create_tasks_prompt = get_prompt(prompt_name="createDailyTasks", label="production")
    return create_tasks_prompt

def get_tasks(user_id: str):
    return ""

def update_tasks(): ...

def delete_tasks(): ...

print(create_tasks("a"))
