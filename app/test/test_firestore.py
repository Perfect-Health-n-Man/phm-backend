from google.cloud import firestore

from app.chat.chat_repository import get_chat_history, FirestoreChatMessageHistory

fs_aclient = firestore.AsyncClient()

def test_get_chat_history():
    result = get_chat_history("WH3FePgXPScZGKoJ0qIQ")
    assert type(result) is FirestoreChatMessageHistory
    assert type(result.to_history_str()) is str