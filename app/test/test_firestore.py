from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from google.cloud import firestore

from app.firestore import firestore_service

fs_client = firestore.Client()
fs_aclient = firestore.AsyncClient()

def test_get_chat_history():
    result = firestore_service.get_chat_history(fs_client, "WH3FePgXPScZGKoJ0qIQ")
    assert type(result) is FirestoreChatMessageHistory

def test_get_user():
    result = firestore_service.get_user(fs_aclient, "rBHLdsDtxqdrGWkisunX")
    assert type(result) is firestore.AsyncDocumentReference