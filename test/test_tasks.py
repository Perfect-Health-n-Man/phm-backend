import pytest

from dotenv import load_dotenv
from langchain_core.messages import AIMessage

load_dotenv()
from google.cloud import firestore
from langfuse import Langfuse

from chat.tasks import crud
from firestore import firestore_crud

lf_client = Langfuse()
fs_aclient = firestore.AsyncClient()
doc_ref = firestore_crud.get_user(fs_aclient, "user-id")
fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    result = await crud.create_tasks(doc_ref, lf_client)
    assert type(result) is AIMessage
    # await history.aadd_messages([result])
