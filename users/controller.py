from flask import Blueprint, request, jsonify,make_response,g
from users.service import register_or_update_user, get_user, delete_user, UserCRUD
from db import db
import json
users_bp = Blueprint('users', __name__)

@users_bp.route('/<uid>/info', methods=['POST','PUT'])
def update_users():
    try:
        # 初期登録チェック
        user_info = request.get_json()
        required_fields = ['name', 'email', 'birthday', 'gender', 'height', 'weight', 'goals']
        missing_fields = [field for field in required_fields if field not in user_info]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # ユーザー登録処理
        user_id = getattr(g, 'user_id')
        user = UserCRUD(fs_aclient=db, user_id=user_id)
        response, status_code = user.register_or_update_user(user_info)
        return jsonify(response),status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<string:uid>/info', methods=['GET'])
def get_user_info(user_id: str):
    try:
        user = UserCRUD(fs_aclient=db, user_id=user_id)
        response, status_code = user.get_user()
        response_json = json.dumps(response, ensure_ascii=False, indent=4)
        return make_response(response_json + "\n", status_code, {"Content-Type": "application/json; charset=utf-8"})

    except Exception as e:
        error_response = json.dumps({"error": str(e)}, ensure_ascii=False, indent=4)
        return make_response(error_response + "\n", 500, {"Content-Type": "application/json; charset=utf-8"})

@users_bp.route('/<string:uid>/info', methods=['DELETE'])
def delete_user_info(user_id: str):
    try:
        user = UserCRUD(fs_aclient=db, user_id=user_id)
        response, status_code = user.delete_user()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500