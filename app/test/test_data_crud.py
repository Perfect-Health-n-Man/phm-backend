import uuid
from datetime import datetime

import pytest
from dotenv import load_dotenv

from app.chat.agent.agent import CreateAgentAnswer
from app.chat.agent.model import State
from app.chat.chat_dto import ChatDto
from app.chat.chat_repository import get_chat_history
from app.chat.data_crud.factory import DataCRUDFactory
from app.firestore import client
from app.firestore.firestore_service import get_user_info_and_tasks

load_dotenv()
user_id = "9OhWsc1l3bM2s4eCUqpW"
history = get_chat_history(user_id)
history.clear()
session_id = "test_normal_chat"+uuid.uuid4().hex
factory = DataCRUDFactory(session_id)
agent = CreateAgentAnswer(
    history=history,
    user_message="",
    fs_aclient=client,
    user_id=user_id,
)

# @pytest.mark.asyncio(loop_scope="session")
# async def test_get_data():
#     await agent.create_daily_logs()
#     data = await factory.get_data(user_id)
#     assert type(data) is dict

@pytest.mark.asyncio(loop_scope="session")
async def test_data_c():
    user_info, task = await get_user_info_and_tasks(user_id)
    state = State(
        user_message="今日は6時に起きた",
        history=get_chat_history(user_id).to_history_str(),
        datetimeNow=datetime.now().isoformat(),
        tasks=task,
        user_info=user_info,
        session_id=session_id,
        user_id=user_id
    )
    data = {
        "diary": "test",
        "meals": dict(),
        "sleep": dict(),
        "exercises": dict(),
    }
    today = datetime.now().strftime('%Y-%m-%d')
    await agent.fs_aclient.document("users", user_id, "daily_logs", today).set(data)
    result = await factory.create_ans(state)
    chat_dto = result.get("messages")[-1]
    assert type(chat_dto) is ChatDto
    print("answer", chat_dto.answer)
    data = await client.document("users", user_id, "daily_logs", today).get()
    data = data.to_dict()
    assert data.get("sleep") != dict()

# @pytest.mark.asyncio(loop_scope="session")
# async def test_data_u():
#     user_info, task = await get_user_info_and_tasks(user_id)
#     state = State(
#         user_message="やっぱり起きた時間は6:30だった。",
#         history=get_chat_history(user_id).to_history_str(),
#         datetimeNow=datetime.now().isoformat(),
#         tasks=task,
#         user_info=user_info,
#         session_id=session_id,
#         user_id=user_id
#     )
#     result = await factory.create_ans(state)
#     chat_dto = result.get("messages")[-1]
#     assert type(chat_dto) is ChatDto
#     print("answer", chat_dto.answer)