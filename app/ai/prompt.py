import os

from langfuse import Langfuse
from langfuse.model import TextPromptClient

def get_langfuse_prompt(prompt_name: str) -> TextPromptClient:
    lf_client = Langfuse()
    env = os.getenv("ENVIRONMENT")
    if env == "dev":
        return lf_client.get_prompt(name=prompt_name, label="latest")
    else:
        return lf_client.get_prompt(name=prompt_name, label="production")

def get_prompt_on_startup() -> None:
    lf_client = Langfuse()
    prompt_names = [
        "createDailyTasks",
        # "checkDailyTasks",
        "answerQuestions",
        "selectAgent",
        "checkAnswer",
        "judgeCRUD"
    ]
    env = os.getenv("ENVIRONMENT")
    if env == "dev":
        for prompt in prompt_names:
            lf_client.get_prompt(name=prompt, label="latest")
    else:
        for prompt in prompt_names:
            lf_client.get_prompt(name=prompt, label="production")