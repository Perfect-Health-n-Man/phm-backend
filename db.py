from firebase_admin import firestore, initialize_app
import firebase_admin

# Firebase Admin SDK の初期化
if not firebase_admin._apps:
    initialize_app()

# Firestore クライアントの初期化
db = firestore.client()