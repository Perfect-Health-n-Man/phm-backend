import json
import pytest

from app.firestore.firestore_service import client as fs_aclient
from app.chat.chat_repository import get_chat_history, FirestoreChatMessageHistory
from app.chat.tasks.tasks_service import create_empty_tasks
from app.users.user_model import User
from app.users.users_repository import register_user


def test_get_chat_history():
    result = get_chat_history("WH3FePgXPScZGKoJ0qIQ")
    assert type(result) is FirestoreChatMessageHistory
    assert type(result.to_history_str()) is str

@pytest.mark.asyncio(loop_scope="session")
async def test_document_to_string():
    # today = "2025-02-04"
    # data = {
    #     "diary": "test",
    #     "meals": dict(),
    #     "sleep": dict(),
    #     "exercises": dict(),
    # }
    # await fs_aclient.document("users", "eQdM5ep94sAYAJf5wv0d", "daily_logs", today).create(data)
    today_log = await fs_aclient.document("users", "eQdM5ep94sAYAJf5wv0d", "daily_logs", today).get()
    log_dict = today_log.to_dict()
    assert log_dict["diary"] == "test"
    print(json.dumps(log_dict, indent=2))


@pytest.mark.asyncio(loop_scope="session")
async def test_create_empty_task():
    user_id = "test_user@example.co.jp"
    await register_user(User(
        name="test_name",
        email=user_id,
        gender="男",
        birthday="2002-12-23",
        height=170,
        weight=50,
        goals=["痩せる"]
    ))
    await create_empty_tasks(user_id)
    user = await fs_aclient.collection("users").document(user_id).get()
    user_dict = user.to_dict()
    await fs_aclient.collection("users").document(user_id).delete()
    assert user_dict["tasks"] == []
