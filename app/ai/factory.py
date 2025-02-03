from langchain_core.prompts import ChatPromptTemplate

from .model import get_llm_model_and_callback
from .prompt import get_langfuse_prompt


class BaseChatFactory:
    def __init__(
            self,
            prompt_name: str,
            output_parser,
            session_id: str,
        ):
        self.prompt = self.get_prompt(prompt_name)
        model, langfuse_handler = get_llm_model_and_callback(session_id=session_id)
        self.model = model
        self.output_parser = output_parser
        self.langfuse_handler = langfuse_handler

    @staticmethod
    def get_prompt(prompt_name: str) -> ChatPromptTemplate:
        system_prompt = get_langfuse_prompt(prompt_name)
        return ChatPromptTemplate.from_template(
            system_prompt.get_langchain_prompt(),
            metadata=dict(langfuse_prompt=system_prompt),
        )

