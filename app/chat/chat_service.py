from typing import Any

from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from app.chat.chat_repository import get_chat_history
from app.chat.normal.factory import NormalChatFactory

async def store_and_respond_chat(uid:str, user_message: str) -> Any:
    try:
        history = get_chat_history(user_id=uid)
        if history is None:
            raise {'error': 'Failed to initialize chat history'}

        normal_chat = NormalChatFactory(history, user_message)
        result = await normal_chat.create_ans()
        result_dict = result.model_dump()

        answer = result_dict.get('answer')
        form = result_dict.get('form')
        return {'answer': answer, 'form': form} if form else {'answer': answer}

    except Exception as e:
        raise Exception(f"Error in store_and_respond_chat: {str(e)}")


async def get_paginated_chats(uid: str, page: int, limit: int = 10) -> list | None:
    try:

        history = get_chat_history(user_id=uid)
        if history is None:
            raise {'error': 'Failed to initialize chat history'}
        messages = await history.aget_messages()

        filtered_messages = []
        for index,msg in enumerate(messages):
            filtered_message = {
                'message_id': index,
                'datetime': msg.additional_kwargs.get("datetime"),
                'message': msg.content,
                'type': msg.type
            }
            filtered_messages.append(filtered_message)

        # メッセージIDで降順ソート（最新のメッセージを先頭に）
        filtered_messages.sort(key=lambda x: x['message_id'], reverse=True)

        # ページネーション処理
        total_messages = len(filtered_messages)
        max_pages = (total_messages + limit - 1) // limit

        if page > max_pages:
            return None

        start = (page - 1) * limit
        end = start + limit

        return filtered_messages[start:end]

    except Exception:
        return None