from quart import Blueprint

chat_bp = Blueprint('chat', __name__)

class RateLimitError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InitializedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NoChatsFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class APIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

from . import chat_controller