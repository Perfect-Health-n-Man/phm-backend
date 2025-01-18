from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from google.cloud import firestore


def get_chat_history(fs_client: firestore.Client, user_id: str) -> FirestoreChatMessageHistory:
    return FirestoreChatMessageHistory(
        session_id=user_id,
        user_id=user_id,
        collection_name="chat_history",
        firestore_client=fs_client
    )


def get_user(fs_aclient: firestore.AsyncClient, user_id: str) -> firestore.AsyncDocumentReference:
    return fs_aclient.document("users", user_id)
