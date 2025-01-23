import pytest

from dotenv import load_dotenv
load_dotenv()

from app.chat.tasks.factory import TasksFactory
from app.chat.tasks.model import Tasks
from app.firestore import firestore_service

fs_aclient = firestore.AsyncClient()
doc_ref = firestore_crud.get_user(fs_aclient, "user-id")
fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    # history.add_message(HumanMessage(content="私のタスクを考えて"))
    tasks = TasksFactory(doc_ref, history)
    result = await tasks.create_tasks()
    assert type(result) is Tasks
    # result_dict = result.model_dump()
    # content = result_dict.get("summary") + "".join(result_dict.get("tasks"))
    # await history.aadd_messages([AIMessage(content=content)])
