import pytest

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
from google.cloud import firestore

from chat.normal.factory import ChatFactory
from chat.normal.model import AIans
from firestore import firestore_crud

# fs_aclient = firestore.AsyncClient()
# doc_ref = firestore_crud.get_user(fs_aclient, "user-id")
fs_client = firestore.Client()
history = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")

@pytest.mark.asyncio
async def test_create_tasks():
    # history.add_message(HumanMessage(content="トマトはどうかな？"))
    normal_chat = ChatFactory(history)
    result = await normal_chat.create_ans()
    assert type(result) is AIans
    result_dict = result.model_dump()
    content = result_dict.get("summary")
    # await history.aadd_messages([AIMessage(content=content)])
