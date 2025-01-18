import pytest

from dotenv import load_dotenv
from langchain_core.messages import AIMessage

load_dotenv()
from google.cloud import firestore

from chat.tasks import crud
from chat.tasks.model import Tasks
from firestore import firestore_crud

fs_aclient = firestore.AsyncClient()
doc_ref = firestore_crud.get_user(fs_aclient, "user-id")
fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    tasks = crud.CRUDTasks(doc_ref)
    result = await tasks.create_tasks()
    assert type(result) is Tasks
    result_dict = result.model_dump()
    content = result_dict.get("summary") + "".join(result_dict.get("tasks"))
    await history.aadd_messages([AIMessage(content=content)])
