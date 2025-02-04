import pytest
from dotenv import load_dotenv
from google.cloud.firestore import AsyncClient

from app.chat.agent.agent import CreateAgentAnswer
from app.chat.chat_dto import ChatDto
from app.chat.chat_repository import get_chat_history
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()
fs_aclient = AsyncClient()
user_id = "test@example.com"
history = get_chat_history(user_id)
history.clear()

agent = CreateAgentAnswer(
    history=history,
    user_message="ヘルシーな肉の種類は？",
    fs_aclient=fs_aclient,
    user_id=user_id,
)

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_info_and_tasks():
    user_info, tasks = await get_user_info_and_tasks(user_id)
    assert type(user_info) == str
    assert type(tasks) == str
    print("user_info: ", user_info)
    print("tasks: ", tasks)

@pytest.mark.asyncio(loop_scope="session")
async def test_root_tasks():
    chat_dto, state = await agent.invoke_graph()
    assert type(chat_dto) is ChatDto
    assert state["current_agent"] == 3
    print("agent_number: ", state["current_agent"])
    print("answer: ", chat_dto.to_str())
    print("number of check: ", len(state["messages"]))
    print("judgement_reason: ", state["judgement_reason"])