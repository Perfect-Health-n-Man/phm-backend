from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()

from app.chat.normal.factory import NormalChatFactory
from app.chat.chat_repository import get_chat_history

@pytest.mark.asyncio(loop_scope="session")
async def test_create_chat():
    user_info, task = await get_user_info_and_tasks("juA4InAftSlGy48HObdW")
    state = State(
        user_message="",
        history=get_chat_history("juA4InAftSlGy48HObdW").to_history_str(),
        datetimeNow=datetime.now().isoformat(),
        tasks=task,
        user_info=user_info,
        session_id="test_normal_chat",
    )
    normal_chat = NormalChatFactory(session_id="test_normal_chat",)
    result = await normal_chat.create_ans(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    print("answer", chat_dto.answer)
    print("tasks->")
    print(*chat_dto.form, sep="\n")
