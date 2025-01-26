import os

from langchain_core.runnables import RunnablePassthrough
from langchain_google_community import VertexAISearchRetriever
from datetime import datetime
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from ai.factory import BaseChatFactory
from .model import AiRagAns


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class RagFactory(BaseChatFactory):
    retriever: VertexAISearchRetriever
    def __init__(self,
                 history: FirestoreChatMessageHistory,
                 user_message: str,
                 ) -> None:
        super().__init__(history, "answerQuestions", AiRagAns, user_message)
        self.retriever = VertexAISearchRetriever(
            project_id=os.getenv("PROJECT_ID"),
            data_store_id=os.getenv("DATA_STORE_ID"),
            max_documents=2,
            max_extractive_answer_count=3,
            get_extractive_answers=True,
        )

    async def create_ans(self):
        add_human_message_task = self.add_user_message()

        chain = (
            RunnablePassthrough.assign(
                context=
                (lambda x: x["question"])
                | self.retriever
                | format_docs
            )
            | self.prompt
            | self.model.with_structured_output(self.output_parser)
        )

        return await self.add_ai_message(
            chain,
            inputs = {
                "input": self.user_message,
                "datetimeNow": datetime.now().isoformat(),
                "chat_history": self.history.messages,
                "question": self.user_message
            },
            add_human_message_task=add_human_message_task
        )