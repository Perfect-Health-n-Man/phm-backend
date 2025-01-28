from langgraph.graph import StateGraph, END

from .model import State, Response, Agent
from app.chat.normal.factory import NormalChatFactory
from app.chat.rag.factory import RagFactory
from app.chat.select.factory import SelectAgent
from app.chat.tasks.factory import TasksFactory

workflow = StateGraph(State)

workflow.add_node("selection", SelectAgent.create_ans())
workflow.add_node("normal_chat", NormalChatFactory.create_ans())
workflow.add_node("rag", RagFactory.create_ans())
workflow.add_node("tasks", TasksFactory.create_tasks())
workflow.add_node("check", check_node)

workflow.set_entry_point("selection")
workflow.add_edge("selection", "normal_chat")
workflow.add_edge("selection", "rag")
workflow.add_edge("selection", "tasks")
workflow.add_edge("normal_chat", "check")
workflow.add_edge("rag", "check")
workflow.add_edge("tasks", "check")
workflow.add_conditional_edges(
    "check",
    lambda state: state.current_judge,
    {True: END, False: "selection"}
)

compiled = workflow.compile()