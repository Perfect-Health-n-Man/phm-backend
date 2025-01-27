import pytest
from dotenv import load_dotenv
load_dotenv()

from google.cloud import firestore

from app.chat.normal.factory import NormalChatFactory
from app.chat.normal.model import AiAns
from app.chat.chat_repository import get_chat_history

fs_client = firestore.Client()
history = get_chat_history("WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_chat():
    normal_chat = NormalChatFactory(
        history,
        user_message="栄養価の高い肉は？",
    )
    result = await normal_chat.create_ans()
    assert type(result) is AiAns
