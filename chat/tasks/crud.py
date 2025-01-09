from langchain_core.messages import HumanMessage

from langfuse.prompt import get_prompt




def create_tasks(user_info):
    create_tasks_prompt = get_prompt(prompt_name="create_tasks", label="production")
    return ""

def read_tasks(): ...

def update_tasks(): ...

def delete_tasks(): ...