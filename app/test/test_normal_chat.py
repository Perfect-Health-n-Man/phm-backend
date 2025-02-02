from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto

load_dotenv()

from app.chat.normal.factory import NormalChatFactory
from app.chat.chat_repository import get_chat_history

state = State(
    user_message="栄養価の高い肉は",
    history=get_chat_history("WH3FePgXPScZGKoJ0qIQ").to_history_str(),
    datetimeNow=datetime.now().isoformat(),
)

@pytest.mark.asyncio
async def test_create_chat():
    normal_chat = NormalChatFactory()
    result = await normal_chat.create_ans(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    print("answer", chat_dto.answer)
    print("tasks->")
    print(*chat_dto.form, sep="\n")
