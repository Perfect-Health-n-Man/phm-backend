import asyncio
import uuid
from asyncio import gather
from datetime import datetime
from typing import Any

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
from ..data_crud.factory import DataCRUDFactory
from ...firestore.firestore_service import get_user_info_and_tasks


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
        session_id = str(uuid.uuid4())
        select_agent_node = SelectAgentFactory(session_id)
        normal_chat_node = NormalChatFactory(session_id)
        rag_node = RagFactory(session_id)
        task_node = TasksFactory(session_id)
        check_node = CheckFactory(session_id)
        data_crud_node = DataCRUDFactory(session_id)

        workflow = StateGraph(State)

        workflow.add_node("selection_node", select_agent_node.create_ans)
        workflow.add_node("normal_chat_node", normal_chat_node.create_ans)
        workflow.add_node("rag_node", rag_node.create_ans)
        workflow.add_node("tasks_node", task_node.create_tasks)
        workflow.add_node("check_node", check_node.create_ans)
        workflow.add_node("data_crud_node", data_crud_node.create_ans)

        workflow.set_entry_point("selection_node")
        workflow.add_conditional_edges(
            "selection_node",
            lambda state: state.current_agent,
            {
                1: "tasks_node",
                2: "data_crud_node",
                3: "rag_node",
                4: "normal_chat_node",
            }
        )
        workflow.add_edge("normal_chat_node", "check_node")
        workflow.add_edge("rag_node", "check_node")
        workflow.add_edge("tasks_node", "check_node")
        workflow.add_edge("data_crud_node", "check_node")
        workflow.add_conditional_edges(
            "check_node",
            lambda state: state.current_judge,
            {
                True: END,
                False: "selection_node"
            }
        )
        self.compiled = workflow.compile()

    async def create_daily_logs(self) -> Any:
        today = datetime.now().strftime('%Y-%m-%d')
        doc_ref = await self.fs_aclient.document("users", self.user_id, "daily_logs", today).get()
        if doc_ref.to_dict():
            return await asyncio.sleep(0.1)
        data = {
            "diary": "",
            "meals": dict(),
            "sleep": dict(),
            "exercises": dict()
        }
        return await self.fs_aclient.document("users", self.user_id, "daily_logs", today).create(data)

    async def invoke_graph(self, add_user_message: bool) -> tuple[ChatDto, State]:
        get_user_info_and_tasks_task = get_user_info_and_tasks(self.user_id)
        create_daily_logs_task = self.create_daily_logs()
        self.history.load_messages()
        if add_user_message:
            add_human_message_task = self.history.aadd_messages([HumanMessage(
                content=self.user_message,
                additional_kwargs={'datetime':datetime.now()})]
            )
        else:
            add_human_message_task = asyncio.sleep(0.1)

        (user_info, tasks), _ = await gather(get_user_info_and_tasks_task, create_daily_logs_task)
        initial_state = State(
            user_message=self.user_message,
            history=self.history.to_history_str(),
            datetimeNow=datetime.now().isoformat(),
            user_info=user_info,
            tasks=tasks,
            session_id=uuid.uuid4().hex,
            user_id=self.user_id,
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
