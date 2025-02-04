import json
from firebase_admin import firestore_async

client = firestore_async.client()

async def get_user_info_and_tasks(user_id: str):
    user_ref = await client.document("users", user_id).get()
    user_dict = user_ref.to_dict()
    user_info = user_dict["user_info"]
    tasks = user_dict["tasks"]
    return json.dumps(user_info, indent=2), "\n".join(tasks)