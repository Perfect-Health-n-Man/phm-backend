from quart import g,jsonify
from app.chat.tasks import task_bp, NoTasksFoundError
from app.chat.tasks.tasks_service import get_tasks


@task_bp.route('/', methods=['GET'],strict_slashes=False)
async def return_tasks_list():
    try:
        user_id = g.user.id
        tasks = await get_tasks(user_id)
        print(tasks)
        return jsonify(tasks=tasks)
    except NoTasksFoundError as e:
        return jsonify({'error': str(e)}),404
    except Exception as e:
        return jsonify({'error': str(e)}),500
