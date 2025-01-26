import pytest

from dotenv import load_dotenv
load_dotenv()
from google.cloud import firestore

from app.chat.tasks.factory import TasksFactory
from app.chat.tasks.model import Tasks
from app.firestore import firestore_service

fs_aclient = firestore.AsyncClient()
doc_ref = firestore_service.get_user(fs_aclient, "rBHLdsDtxqdrGWkisunX")
fs_client = firestore.Client()
history = firestore_service.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    tasks = TasksFactory(doc_ref, history)
    result = await tasks.create_tasks()
    assert type(result) is Tasks
    print("summary", result.summary)
    print("tasks->")
    print(*result.tasks, sep="\n")
