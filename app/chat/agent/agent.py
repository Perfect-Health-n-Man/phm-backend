from asyncio import gather
from datetime import datetime

from google.cloud.firestore import AsyncClient
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from .model import State, to_ai_response
from app.chat.normal.factory import NormalChatFactory
from app.chat.rag.factory import RagFactory
from app.chat.select.factory import SelectAgentFactory
from app.chat.tasks.factory import TasksFactory
from app.chat.check.factory import CheckFactory
from ..chat_dto import ChatDto
from ..chat_repository import FirestoreChatMessageHistory


class CreateAgentAnswer:
    compiled: CompiledStateGraph
    def __init__(
            self,
            history: FirestoreChatMessageHistory,
            user_message: str,
            fs_aclient: AsyncClient,
            user_id: str,
        ):
        self.history = history
        self.user_message = user_message
        self.fs_aclient = fs_aclient
        self.user_id = user_id

    def _create_graph(self) -> None:
        select_agent_node = SelectAgentFactory()
        normal_chat_node = NormalChatFactory()
        rag_node = RagFactory()
        task_node = TasksFactory(
            fs_aclient=self.fs_aclient,
            user_id=self.user_id
        )
        check_node = CheckFactory()

        workflow = StateGraph(State)

        workflow.add_node("selection", select_agent_node.create_ans)
        workflow.add_node("normal_chat", normal_chat_node.create_ans)
        workflow.add_node("rag", rag_node.create_ans)
        workflow.add_node("tasks", task_node.create_tasks)
        workflow.add_node("check", check_node.create_ans)

        workflow.set_entry_point("selection")
        workflow.add_conditional_edges(
            "selection",
            lambda state: state.current_agent,
            {
                1: "tasks",
                # 2: "",
                3: "rag",
                4: "normal_chat",
            }
        )
        workflow.add_edge("normal_chat", "check")
        workflow.add_edge("rag", "check")
        workflow.add_edge("tasks", "check")
        workflow.add_conditional_edges(
            "check",
            lambda state: state.current_judge,
            {
                True: END,
                False: "selection"
            }
        )
        self.compiled = workflow.compile()

    async def invoke_graph(self) -> tuple[ChatDto, State]:
        self.history.load_messages()
        add_human_message_task = self.history.aadd_messages([HumanMessage(
            content=self.user_message,
            additional_kwargs={'datetime':datetime.now()})]
        )

        initial_state = State(
            user_message=self.user_message,
            history=self.history.to_history_str(),
            datetimeNow=datetime.now().isoformat()
        )
        self._create_graph()
        chain_invoke_task = self.compiled.ainvoke(initial_state)

        _, result_state = await gather(add_human_message_task, chain_invoke_task)
        ai_response = to_ai_response(result_state)

        await self.history.aadd_messages([AIMessage(
            content=ai_response.to_str(),
            additional_kwargs={'datetime':datetime.now()})]
        )
        return ai_response, result_state
