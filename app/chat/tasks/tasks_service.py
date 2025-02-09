from app.chat.tasks import NoTasksFoundError
from app.firestore import client


async def get_tasks(user_id: str) -> list | None:
    try:
        user_data = await client.collection("users").document(user_id).get()
        user = user_data.to_dict()
        tasks = user.get("tasks")
        if tasks is None:
            raise NoTasksFoundError('No tasks found')
        return tasks
    except NoTasksFoundError as e:
        raise e
    except Exception as e:
        raise e

async def create_empty_tasks(user_id: str) -> None:
    doc_ref = client.collection('users').document(user_id)
    await doc_ref.set({'tasks': []}, merge=True)
