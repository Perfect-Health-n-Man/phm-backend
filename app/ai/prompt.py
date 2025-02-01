from langfuse import Langfuse
from langfuse.model import TextPromptClient

def get_langfuse_prompt(prompt_name: str) -> TextPromptClient:
    lf_client = Langfuse()
    return lf_client.get_prompt(name=prompt_name, label="production")

def get_prompt_on_startup() -> None:
    lf_client = Langfuse()
    prompt_names = [
        "createDailyTasks",
        # "checkDailyTasks",
        "answerQuestions",
        "selectAgent",
        "checkAnswer",
    ]
    for prompt in prompt_names:
        lf_client.get_prompt(name=prompt, label="production")