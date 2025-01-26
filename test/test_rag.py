import pytest
from dotenv import load_dotenv
load_dotenv()

from google.cloud import firestore

from chat.rag.factory import RagFactory
from chat.rag.model import AiRagAns
from firestore import firestore_crud

fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_rag():
    rag_chat = RagFactory(
        history,
        user_message="栄養価の高い野菜は？",
    )
    result = await rag_chat.create_ans()
    assert type(result) is AiRagAns
    print("cot", result.cot)
    print("rag", result.rag)
    print("summary", result.summary)