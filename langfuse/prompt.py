# langfuse
import requests
import os
from typing import Optional

def get_prompt(
        prompt_name: str,
        version: Optional[int] = None,
        label: Optional[str] = None):
    # エンドポイントURL
    url = f"{os.environ['LANGFUSE_HOST']}/api/public/v2/prompts/{prompt_name}"

    # 認証情報
    username = os.environ['LANGFUSE_PUBLIC_KEY']
    password = os.environ['LANGFUSE_SECRET_KEY']

    # クエリパラメータの設定
    params = {}
    if version is not None:
        params['version'] = version
    if label is not None:
        params['label'] = label

    # ヘッダー
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # GETリクエストの実行
        response = requests.get(
            url=url,
            params=params,
            headers=headers,
            auth=(username, password)
        )

        # レスポンスの確認
        if 200 <= response.status_code < 300:
            print("リクエスト成功")
            return response.json()
        else:
            print(f"エラー: ステータスコード {response.status_code}")
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"リクエスト中にエラーが発生しました: {e}")
        return None