from datetime import datetime

import pytest

from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()
from google.cloud import firestore

from app.chat.tasks.factory import TasksFactory
from app.chat.chat_repository import get_chat_history

fs_aclient = firestore.AsyncClient()

@pytest.mark.asyncio(loop_scope="session")
async def test_create_tasks():
    user_id = "uEG2dFgAi7ethrJ3qPg3"
    user_info, task = await get_user_info_and_tasks(user_id)
    state = State(
        user_message="",
        history=get_chat_history(user_id).to_history_str(),
        datetimeNow=datetime.now().isoformat(),
        tasks=task,
        user_info=user_info,
        session_id="test_tasks",
        user_id=user_id
    )
    tasks = TasksFactory(session_id="test_tasks")
    result = await tasks.create_tasks(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    print("answer", chat_dto.answer)
    print("tasks->")
    print(*chat_dto.form, sep="\n")

# @pytest.mark.asyncio(loop_scope="session")
# async def test_update_firestore():
    # a = await fs_aclient.document("users"+"/testy@example.com").get()
    # print(a.to_dict())
    # doc_ref = fs_aclient.document("users/" + "testy@example.com")
    # await doc_ref.update({"tasks": ["test", "test2"]})