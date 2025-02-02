from app.chat.agent.agent import CreateAgentAnswer
from app.chat.chat_dto import ChatDto
from app.chat.chat_repository import get_chat_history
from app.firestore import client


async def store_and_respond_chat(user_id:str, user_message: str) -> ChatDto:
    try:
        history = get_chat_history(user_id=user_id)
        if history is None:
            raise {'error': 'Failed to initialize chat history'}

        fs_aclient = client
        agent_chain = CreateAgentAnswer(
            history=history,
            user_message=user_message,
            fs_aclient=fs_aclient,
            user_id=user_id,
        )
        chat_dto, _ = await agent_chain.invoke_graph()
        return chat_dto

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