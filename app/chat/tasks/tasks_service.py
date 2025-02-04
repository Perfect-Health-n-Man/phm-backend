from firebase_admin import firestore_async

from app.chat.tasks import NoTasksFoundError


async def get_tasks(user_id: str) -> list | None:
    try:
        client = firestore_async.client()
        user_data = await client.collection("users").document(user_id).get()
        print(user_data)
        user = user_data.to_dict()
        print(user)
        tasks = user.get("tasks")
        if tasks is None:
            raise NoTasksFoundError('No tasks found')
        return tasks
    except NoTasksFoundError as e:
        raise e
    except Exception as e:
        raise e