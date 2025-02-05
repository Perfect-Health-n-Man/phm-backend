import os

from langchain_core.runnables import RunnablePassthrough
from langchain_google_community import VertexAISearchRetriever
from datetime import datetime

from app.ai.factory import BaseChatFactory
from .model import AiRagAns
from ..agent.model import State
from ..chat_dto import ChatDto


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class RagFactory(BaseChatFactory):
    retriever: VertexAISearchRetriever
    def __init__(self, session_id: str) -> None:
        super().__init__("answerQuestions", AiRagAns, session_id)
        self.retriever = VertexAISearchRetriever(
            project_id=os.getenv("PROJECT_ID"),
            data_store_id=os.getenv("DATA_STORE_ID"),
            max_documents=2,
            max_extractive_answer_count=3,
            get_extractive_answers=True,
            beta=True,
        )

    async def create_ans(self, state: State) -> dict[str, list[ChatDto]]:
        chain = (
                RunnablePassthrough.assign(
                    context=
                    (lambda x: x["user_message"])
                    | self.retriever
                    | format_docs
                )
                | self.prompt
                | self.model.with_structured_output(self.output_parser)
        )
        result: AiRagAns = await chain.ainvoke(
            input={
                "input": state.user_message,
                "datetimeNow": datetime.now().isoformat(),
                "chat_history": "",#RAGのときはhistoryを読まない
                "user_message": state.user_message,
                "user_info": state.user_info,
                "tasks": state.tasks,
                "daily_logs": "",
            },
            config={"callbacks": [self.langfuse_handler]}
        )
        return {"messages": [ChatDto(answer=result.answer, form=result.form)]}
