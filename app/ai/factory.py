from asyncio import gather
from datetime import datetime
from typing import Any, Coroutine

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from langchain_core.runnables import Runnable

from .model import get_llm_model_and_callback
from .prompt import get_langchain_prompt

class BaseChatFactory:
    def __init__(
            self,
            history: FirestoreChatMessageHistory,
            prompt_name: str,
            output_parser,
            user_message: str
        ):
        self.history = history
        system_prompt = get_langchain_prompt(prompt_name)
        prompt = ChatPromptTemplate.from_template(
            system_prompt.get_langchain_prompt(),
            metadata=dict(langfuse_prompt=system_prompt),
        )
        self.prompt = prompt
        model, langfuse_handler = get_llm_model_and_callback()
        self.model = model
        self.output_parser = output_parser
        self.langfuse_handler = langfuse_handler
        self.user_message = user_message

    async def add_user_message(self, ):
        self.history.load_messages()
        return await self.history.aadd_messages([HumanMessage(content=self.user_message, additional_kwargs={'datetime':datetime.now()})])

    async def add_ai_message(
            self,
            chain: Runnable[dict[str, Any], Any],
            inputs: dict[str, Any],
            add_human_message_task: Coroutine[Any, Any, None]
        ) -> Any:
        chain_invoke_task = chain.ainvoke(
            input=inputs,
            config={"callbacks":[self.langfuse_handler]}
        )
        _, ai_message = await gather(add_human_message_task, chain_invoke_task)
        ai_message_summary = ai_message.model_dump().get("summary")
        self.history.add_message(AIMessage(content=ai_message_summary, additional_kwargs={'datetime':datetime.now()}))
        return ai_message

