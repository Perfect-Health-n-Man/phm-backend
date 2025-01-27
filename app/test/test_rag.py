import pytest
from dotenv import load_dotenv
load_dotenv()

from google.cloud import firestore

from app.chat.rag.factory import RagFactory
from app.chat.rag.model import AiRagAns
from app.chat.chat_repository import get_chat_history

fs_client = firestore.Client()
history = get_chat_history("NBCciQVahlCczQUzAM9F")

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
    print("answer", result.answer)