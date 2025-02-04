from app.chat.tasks.tasks_service import create_empty_tasks
from app.chat.chat_service import store_and_respond_chat
from app.users import users_repository
from app.users.user_model import User

async def register_or_update_user(user: dict) -> None:
    # {userId}ドキュメントをアップデートする（無ければ作成する）
    current_user = await users_repository.get_user(user['email'])
    if current_user:
        await users_repository.update_user(User.from_json(user))
    else:
        _, doc_ref = await users_repository.register_user(User.from_json(user))
        await store_and_respond_chat(doc_ref.id, "タスク作成のために必要な質問をしてください。")
        await create_empty_tasks(user['email'])

async def get_user(user_id: str) -> User | None:
    return await users_repository.get_user(user_id)

def validate_user(user_info: dict) -> bool:
    required_fields = ['name', 'email', 'birthday', 'gender', 'height', 'weight', 'goals']
    missing_fields = [field for field in required_fields if field not in user_info]
    return not missing_fields
