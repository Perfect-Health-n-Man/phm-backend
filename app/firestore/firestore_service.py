from firebase_admin import firestore_async

client = firestore_async.client()






from google.cloud import firestore


def get_user(fs_aclient: firestore.AsyncClient, user_id: str) -> firestore.AsyncDocumentReference:
    return fs_aclient.document("users", user_id)