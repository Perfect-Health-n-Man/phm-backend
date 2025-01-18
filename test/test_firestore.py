import pytest

from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from google.cloud import firestore

from firestore import firestore_crud

fs_client = firestore.Client()
fs_aclient = firestore.AsyncClient()

def test_get_chat_history():
    result = firestore_crud.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")
    assert type(result) is FirestoreChatMessageHistory

def test_get_user():
    result = firestore_crud.get_user(fs_aclient, "user-id")
    assert type(result) is firestore.AsyncDocumentReference