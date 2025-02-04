from quart import Blueprint

task_bp = Blueprint('task', __name__)

class NoTasksFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

from . import tasks_controller
