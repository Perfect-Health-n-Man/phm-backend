from datetime import datetime

import pytest

from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto

load_dotenv()
from google.cloud import firestore

from app.chat.tasks.factory import TasksFactory
from app.chat.chat_repository import get_chat_history

fs_aclient = firestore.AsyncClient()
state = State(
    user_message="",
    history=get_chat_history("juA4InAftSlGy48HObdW").to_history_str(),
    datetimeNow=datetime.now().isoformat()
)

@pytest.mark.asyncio
async def test_create_tasks():
    tasks = TasksFactory(fs_aclient, user_id="rBHLdsDtxqdrGWkisunX")
    result = await tasks.create_tasks(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    print("answer", chat_dto.answer)
    print("tasks->")
    print(*chat_dto.form, sep="\n")
