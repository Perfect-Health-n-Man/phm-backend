import pytest

from dotenv import load_dotenv
load_dotenv()
from google.cloud import firestore
from langfuse import Langfuse

from chat.tasks import crud

fs_aclient = firestore.AsyncClient()
lf_client = Langfuse()

@pytest.mark.asyncio
async def test_create_tasks():
    result = await crud.create_tasks(fs_aclient, lf_client, "user-id")
    assert type(result) is str
