from requests import get, exceptions, models
import os
from typing import Optional
import config

def get_prompt(
        prompt_name: str,
        version: Optional[int] = None,
        label: Optional[str] = None) -> models.Response|None:
    # エンドポイントURL
    url = f"{config.LANGFUSE_HOST}/api/public/v2/prompts/{prompt_name}"

    # 認証情報
    username = config.LANGFUSE_PUBLIC_KEY
    password = config.LANGFUSE_SECRET_KEY

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
        response = get(
            url=url,
            params=params,
            headers=headers,
            auth=(username, password)
        )

        # レスポンスの確認
        if 200 <= response.status_code < 300:
            print("リクエスト成功")
            return response
        else:
            print(f"エラー: ステータスコード {response.status_code}")
            return response

    except exceptions.RequestException as e:
        print(f"リクエスト中にエラーが発生しました: {e}")
        return None