from flask import request,g
from auth.service import verify_token

def authenticate_request():
    # リクエストヘッダーからトークンを取得
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise Exception("Authorization header is missing or invalid")

    # トークンの検証
    id_token = auth_header.split('Bearer ')[1]
    user_id = verify_token(id_token)
    if not user_id:
        raise Exception("Invalid token")

    # ユーザーIDをリクエストコンテキストに保存
    g.user_id = user_id