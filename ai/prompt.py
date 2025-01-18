from langfuse import Langfuse
from langchain_core.prompts import ChatPromptTemplate

def get_langchain_prompt(prompt_name: str):
    lf_client = Langfuse()
    langfuse_prompt = lf_client.get_prompt(name=prompt_name, label="production")
    langchain_prompt = ChatPromptTemplate(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )
    return langchain_prompt

def get_prompt_on_startup():
    lf_client = Langfuse()
    prompt_names = [
        "createDailyTasks",
        "checkDailyTasks",
    ]
    for prompt in prompt_names:
        lf_client.get_prompt(name=prompt, label="production")