from firebase_admin import auth
from quart import request

def verify_token(id_token) -> str:
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise e

def get_email_by_user_id(user_id: str) -> str:
     user = auth.get_user(user_id)
     return user.email

def get_id_token_from_request() -> str:
    # リクエストヘッダーからトークンを取得
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise Exception("Authorization header is missing or invalid")
    return auth_header.split('Bearer ')[1]