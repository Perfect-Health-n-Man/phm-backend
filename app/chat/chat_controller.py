from quart import request, g
from app.firestore.firestore_service import client
from app.chat.chat_repository import get_chat_history
from app.chat.chat_service import store_and_respond_chat, get_paginated_chats
from app.chat import chat_bp

@chat_bp.route('/', methods=['POST'])
async def handle_chat():
    try:
        data = await request.get_json()
        user_message = data.get('message')
        uid = g.user.id
        if not user_message:
            return {"error": "message is required"}, 400

        history = get_chat_history(uid)

        if history is None:
            return {"error": "Failed to initialize chat history"}, 500
        ai_response = await store_and_respond_chat(history, user_message)
        return {"response": ai_response}, 201

    except Exception as e:
        return {"error": str(e)}, 500


@chat_bp.route('/', methods=['GET'])
async def get_chat_list():
    try:
        uid = g.user_id
        page = request.args.get('pages', default=1, type=int)
        limit = 10

        chat_ref = client
        chats_list = await get_paginated_chats(uid, chat_ref, page, limit)

        if chats_list:
            return {"page": page, "chats": chats_list}, 200
        else:
            return {"message": "No chats found."}, 404

    except Exception as e:
        return {"error": str(e)}, 500