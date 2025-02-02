from quart import Quart, jsonify, g
from app.auth import get_id_token_from_request, verify_token
from app.auth.service import get_email_by_uid


def register_before_request(app: Quart):
    @app.before_request
    def before_request():
        try:
            id_token = get_id_token_from_request()
            uid = verify_token(id_token)
            email = get_email_by_uid(uid)
            g.user_id = email
        except Exception as e:
            return jsonify({"error": str(e)}), 401
