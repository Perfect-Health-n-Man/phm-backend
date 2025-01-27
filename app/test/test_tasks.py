import pytest

from dotenv import load_dotenv
load_dotenv()
from google.cloud import firestore

from app.chat.tasks.factory import TasksFactory
from app.chat.tasks.model import Tasks
from app.chat.chat_repository import get_chat_history
from app.firestore.firestore_service import get_user

fs_aclient = firestore.AsyncClient()
doc_ref = get_user(fs_aclient, "rBHLdsDtxqdrGWkisunX")
fs_client = firestore.Client()
history = get_chat_history("juA4InAftSlGy48HObdW")

@pytest.mark.asyncio
async def test_create_tasks():
    tasks = TasksFactory(doc_ref, history)
    result = await tasks.create_tasks()
    assert type(result) is Tasks
    print("answer", result.answer)
    print("tasks->")
    print(*result.answer, sep="\n")
