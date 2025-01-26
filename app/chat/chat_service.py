from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import FirestoreChatMessageHistory
from app.chat.chat_repository import get_chat_history
from app.chat.normal.factory import ChatFactory


async def store_and_respond_chat(history: FirestoreChatMessageHistory, user_message: str) -> str | None:
    try:
        # 同期的に処理
        history.add_message(HumanMessage(content=user_message, additional_kwargs={'datetime':datetime.now()}))

        normal_chat = ChatFactory(history)
        result = await normal_chat.create_ans()
        result_dict = result.model_dump()
        content = result_dict.get("summary")

        # 同期的に処理
        history.add_messages([AIMessage(content=content, additional_kwargs={'datetime':datetime.now()})])

        if content is None:
            raise "Summary content is missing in 'store_and_respond_chat'"
        return content
    except Exception as e :
        raise e


async def get_paginated_chats(uid: str, page: int, limit: int = 10) -> list | None:
    try:

        history = get_chat_history(user_id=uid)
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
    except Exception as e:
        raise e
