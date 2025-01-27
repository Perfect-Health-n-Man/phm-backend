from quart import request, g
from app.chat.chat_service import store_and_respond_chat, get_paginated_chats
from app.chat import chat_bp

@chat_bp.route('/', methods=['POST'])
async def handle_chat():
    try:
        data = await request.get_json()
        user_message = data.get('message')
        if not user_message or not hasattr(g,'user_id'):
            return {"error": "user_id or message is empty"}, 400

        uid = g.user_id

        ai_response = await store_and_respond_chat(uid, user_message)

        if not ai_response:
            return {"error": "Encountered an internal error while executing the 'store_and_respond_chat' function. "}, 500
        return {"response": ai_response}, 201

    except Exception as e:
        return {"error": str(e)}, 500


@chat_bp.route('/', methods=['GET'])
async def get_chat_list():
    try:
        if not hasattr(g, 'user_id'):
            return {"error": "user_id is empty"}, 400
        uid = g.user_id
        page = request.args.get('pages', default=1, type=int)
        limit = 10

        chats_list = await get_paginated_chats(uid, page, limit)

        if chats_list:
            return {"page": page, "chats": chats_list}, 200
        else:
            return {"message": "No chats found."}, 404

    except Exception as e:
        return {"error": {str(e)}}, 500