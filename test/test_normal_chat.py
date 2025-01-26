import pytest
from dotenv import load_dotenv
load_dotenv()

from google.cloud import firestore

from chat.normal.factory import NormalChatFactory
from chat.normal.model import AiAns
from firestore import firestore_crud

fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_chat():
    normal_chat = NormalChatFactory(
        history,
        user_message="栄養価の高い野菜は？",
        prompt_name="answerQuestions"
    )
    result = await normal_chat.create_ans()
    assert type(result) is AiAns
