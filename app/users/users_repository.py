from typing import Any

from google.cloud.firestore_v1 import AsyncDocumentReference

from app.firestore import client
from app.users.user_model import User

async def get_user(user_id: str) -> User | None:
    user_data = await client.document("users", user_id).get()
    if user_data.exists is False: return None
    user = user_data.to_dict()
    user_info = user["user_info"]
    return User(
        name=user_info["name"],
        email=user_info["email"],
        gender=user_info["gender"],
        birthday=user_info["birthday"],
        height=user_info["height"],
        weight=user_info["weight"],
        goals=user_info["goals"]
    )

async def register_user(user: User) -> tuple[Any, AsyncDocumentReference]:
    return await client.collection("users").add(user.to_dict(), document_id=user.email)

async def update_user(user: User):
    return await client.document("users", user.email).update(user.to_dict())
