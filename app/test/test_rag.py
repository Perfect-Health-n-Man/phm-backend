from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto

load_dotenv()

from app.chat.rag.factory import RagFactory
from app.chat.chat_repository import get_chat_history

state = State(
    user_message="栄養価の高い野菜は",
    history=get_chat_history("NBCciQVahlCczQUzAM9F").to_history_str(),
    datetimeNow=datetime.now().isoformat()
)

@pytest.mark.asyncio
async def test_rag():
    rag_chat = RagFactory()
    result = await rag_chat.create_ans(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    # print("cot", chat_dto.get("cot"))
    # print("rag", chat_dto.rag)
    print("answer", chat_dto.answer)