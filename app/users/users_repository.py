from firebase_admin import firestore_async
from app.users.user_model import User

async def get_user(user_id: str) -> User | None:
    client = firestore_async.client()
    print(user_id)
    user_data = await client.collection("users").document(user_id).get()
    user_data = user_data.to_dict()
    print(user_data)
    if user_data is None: return None
    return User(
        name=user_data["name"],
        email=user_data["email"],
        gender=user_data["gender"],
        birthday=user_data["birthday"],
        height=user_data["height"],
        weight=user_data["weight"],
        goals=user_data["goals"]
    )

async def register_user(user: User):
    client = firestore_async.client()
    return await client.collection("users").add(user.to_dict(), document_id=user.email)

async def update_user(user: User):
    client = firestore_async.client()
    return await client.collection("users").document(user.email).update(user.to_dict())
