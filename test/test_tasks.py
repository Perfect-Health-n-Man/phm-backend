import pytest

from dotenv import load_dotenv
load_dotenv()
from google.cloud import firestore

from chat.tasks.factory import TasksFactory
from chat.tasks.model import Tasks
from firestore import firestore_crud

fs_aclient = firestore.AsyncClient()
doc_ref = firestore_crud.get_user(fs_aclient, "rBHLdsDtxqdrGWkisunX")
fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    tasks = TasksFactory(doc_ref, history)
    result = await tasks.create_tasks()
    assert type(result) is Tasks
    print("summary", result.summary)
    print("tasks->")
    print(*result.tasks, sep="\n")
