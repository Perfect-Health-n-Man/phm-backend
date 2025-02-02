import pytest
from dotenv import load_dotenv
from google.cloud.firestore import AsyncClient

from app.chat.agent.agent import CreateAgentAnswer
from app.chat.chat_dto import ChatDto
from app.chat.chat_repository import get_chat_history

load_dotenv()
fs_aclient = AsyncClient()
user_id = "rBHLdsDtxqdrGWkisunX"
history = get_chat_history(user_id)
history.clear()

@pytest.mark.asyncio
async def test_root_tasks():
    agent = CreateAgentAnswer(
        history=history,
        user_message="ヘルシーな肉の種類は？",
        fs_aclient=fs_aclient,
        user_id=user_id,
    )
    chat_dto, state = await agent.invoke_graph()
    assert type(chat_dto) is ChatDto
    assert state["current_agent"] == 3
    print("agent_number: ", state["current_agent"])
    print("answer: ", chat_dto.to_str())
    print("number of check: ", len(state["messages"]))
    print("judgement_reason: ", state["judgement_reason"])