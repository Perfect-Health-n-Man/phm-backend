from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()

from app.chat.rag.factory import RagFactory
from app.chat.chat_repository import get_chat_history

@pytest.mark.asyncio(loop_scope="session")
async def test_rag():
    user_id = "LYrr8n0tmPjwyW2Dw2Eg"
    user_info, task = await get_user_info_and_tasks(user_id)
    state = State(
        user_message="",
        history=get_chat_history("LYrr8n0tmPjwyW2Dw2Eg").to_history_str(),
        datetimeNow=datetime.now().isoformat(),
        tasks=task,
        user_info=user_info,
        session_id="test_rag",
        user_id=user_id
    )
    rag_chat = RagFactory(session_id="test_rag")
    result = await rag_chat.create_ans(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    # print("cot", chat_dto.get("cot"))
    # print("rag", chat_dto.rag)
    print("answer", chat_dto.answer)