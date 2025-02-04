import json
from datetime import datetime

import pytest

from app.firestore.firestore_service import client as fs_aclient
from app.chat.chat_repository import get_chat_history, FirestoreChatMessageHistory

def test_get_chat_history():
    result = get_chat_history("WH3FePgXPScZGKoJ0qIQ")
    assert type(result) is FirestoreChatMessageHistory
    assert type(result.to_history_str()) is str

@pytest.mark.asyncio(loop_scope="session")
async def test_document_to_string():
    today = "2025-02-03"
    today_log = await fs_aclient.document("users", "eQdM5ep94sAYAJf5wv0d", "daily_logs", today).get()
    log_dict = today_log.to_dict()
    assert log_dict["diary"] == "test"
    print(json.dumps(log_dict, indent=2))