from langchain_community.chat_message_histories import FirestoreChatMessageHistory


def get_chat_history(user_id: str) -> FirestoreChatMessageHistory:
    try:
        # 非同期クライアントの代わりに同期クライアントを使用
        from firebase_admin import firestore
        client = firestore.client()

        history = FirestoreChatMessageHistory(
            session_id=user_id,
            user_id=user_id,
            collection_name="chat_history",
            firestore_client=client
        )

        return history

    except Exception as e:
        raise