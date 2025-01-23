import asyncio

from flask import Blueprint, jsonify, request,g
from google.cloud.firestore_v1 import DocumentReference
from langchain_community.chat_message_histories import FirestoreChatMessageHistory

from firestore.firestore_crud import get_chat_history
from chat.service import store_and_respond_chat, get_paginated_chats
from db import db


chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/', methods=['POST'])
async def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        uid = getattr(g, 'user_id')
        if not all([user_message, uid]):
            return jsonify({
                'error': 'message, session_id, and user_id are required'
            }), 400

        history = get_chat_history(db, uid)

        ai_response = await store_and_respond_chat(history, user_message)

        return jsonify({
            'response': ai_response
        }), 201

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@chat_bp.route('/', methods=['GET'])
def get_chat_list():
    try:
        uid = getattr(g, 'user_id')
        page = request.args.get('pages', default=1, type=int)
        limit = 10

        # Firestoreのリファレンス取得
        chat_ref = db

        chats_list = get_paginated_chats(uid, chat_ref, page, limit)

        if chats_list:
            return jsonify({"page": page, "chats": chats_list}), 200
        else:
            return jsonify({"message": "No chats found."}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500




