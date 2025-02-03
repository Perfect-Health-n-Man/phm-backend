from quart import request, jsonify, g
from app.users import users_service, users_bp

@users_bp.route('/info', methods=['POST','PUT'], strict_slashes=False)
async def register_or_update_user():
    try:
        user_info = await request.get_json()
        print(user_info["goals"])
        validate_result = users_service.validate_user(user_info)
        if not validate_result:
            return jsonify({"message": "There is missing field"}), 400

        await users_service.register_or_update_user(user_info)
        return jsonify({"message": "User registered"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@users_bp.route('/info', methods=['GET'], strict_slashes=False)
async def get_user_info():
    user_id = g.user_id
    try:
        user = await users_service.get_user(user_id)
        if user is not None:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"message": "User not found"}), 404


    except Exception as e:
        return jsonify({"error": str(e)}), 500