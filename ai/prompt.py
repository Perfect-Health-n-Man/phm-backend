from langfuse import Langfuse
from langchain_core.prompts import ChatPromptTemplate

def get_prompt(lf_client: Langfuse, prompt_name: str):
    langfuse_prompt = lf_client.get_prompt(name=prompt_name, label="production")
    langchain_prompt = ChatPromptTemplate(
        langfuse_prompt.get_langchain_prompt(),
        metadata={"langfuse_prompt": langfuse_prompt},
    )
    return langchain_prompt
