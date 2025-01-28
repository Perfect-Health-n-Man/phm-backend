from langfuse import Langfuse
from langchain_core.messages import SystemMessage
from langfuse.model import TextPromptClient


def get_langchain_prompt(prompt_name: str) -> TextPromptClient:# SystemMessage:
    lf_client = Langfuse()
    return lf_client.get_prompt(name=prompt_name, label="production")
    # return SystemMessage(
    #     content=langfuse_prompt.get_langchain_prompt(),
    #     metadata=dict(langfuse_prompt=langfuse_prompt),
    # )

def get_prompt_on_startup() -> None:
    lf_client = Langfuse()
    prompt_names = [
        "createDailyTasks",
        # "checkDailyTasks",
        "answerQuestions",
        "selectAgent",
    ]
    for prompt in prompt_names:
        lf_client.get_prompt(name=prompt, label="production")