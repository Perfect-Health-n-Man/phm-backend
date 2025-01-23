from langchain_core.prompts import ChatPromptTemplate

from ai.prompt import get_langchain_prompt
from datetime import datetime
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from .model import AIans
from ai.model import get_llm_model_and_callback


class ChatFactory:
    def __init__(self, history: FirestoreChatMessageHistory):
        self.history = history

    async def create_ans(self) -> AIans:
        get_chat_history_task = self.history.aget_messages()
        system_prompt = get_langchain_prompt("answerQuestions")

        model, langfuse_handler = get_llm_model_and_callback()
        output_parser = AIans

        messages = await get_chat_history_task
        messages = [system_prompt] + messages
        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | model.with_structured_output(output_parser)
        return await chain.ainvoke(
            input={"datetimeNow": datetime.now},
            config={"callbacks":[langfuse_handler]}
        )
