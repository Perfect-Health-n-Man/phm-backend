import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from langchain_google_community import VertexAISearchRetriever

from ai.prompt import get_langchain_prompt
from ai.model import get_llm_model_and_callback

class RagFactory:
    retriever: VertexAISearchRetriever

    def __init__(self, history: FirestoreChatMessageHistory) -> None:
        self.history = history
        self.retriever = VertexAISearchRetriever(
            project_id=os.getenv("PROJECT_ID"),
            data_store_id=os.getenv("DATA_STORE_ID"),
            max_documents=2,
        )

    async def create_ans(self) -> AIans:
        get_chat_history_task = self.history.aget_messages()
        system_prompt = get_langchain_prompt("rag")

        model, langfuse_handler = get_llm_model_and_callback()
        output_parser = AIans

        messages = await get_chat_history_task
        messages = [system_prompt] + messages
        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | model.with_structured_output(output_parser)
        return await chain.ainvoke(
            input={"datetimeNow": datetime().now},
            config={"callbacks":[langfuse_handler]}
        )