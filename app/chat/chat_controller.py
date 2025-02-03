from quart import request, g, jsonify
from app.chat.chat_service import store_and_respond_chat, get_paginated_chats
from app.chat import chat_bp, InitializedError, RateLimitError, NoChatsFoundError, APIError


@chat_bp.route('/', methods=['POST'], strict_slashes=False)
async def handle_chat():
    try:
        data = await request.get_json()
        user_message = data.get('message')
        if not user_message or not hasattr(g,'user_id'):
            return {"error": "user_id or message is empty"}, 400

        user_id = g.user_id
        try:
            ai_response = await store_and_respond_chat(user_id, user_message)
            return ai_response.to_json(), 201
        except InitializedError as e:
            return {"error": str(e)}, 500
        except RateLimitError as e:
            return {"error": str(e)}, 429
        except APIError as e:
            return {"error": str(e)}, 500
        except Exception as e:
            return {'error': str(e)}, 500

    except Exception as e:
        return {"error": str(e)}, 500


@chat_bp.route('/', methods=['GET'], strict_slashes=False)
async def get_chat_list():
    try:
        if not hasattr(g, 'user_id'):
            return {"error": "user_id is empty"}, 400
        uid = g.user_id
        page = request.args.get('pages', default=1, type=int)
        limit = 10

        try:
            chats_list = await get_paginated_chats(uid, page, limit)
            return {"page": page, "chats": chats_list}, 200
        except InitializedError as e:
            return {"error": str(e)}, 500
        except NoChatsFoundError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    except Exception as e:
        return {"error": {str(e)}}, 500