from dotenv import load_dotenv
from firebase_admin import initialize_app
initialize_app()
from quart import Quart
from app.ai.prompt import get_prompt_on_startup
from app.brefor_request import register_before_request


def create_app():
    app = Quart(__name__)
    load_dotenv()
    register_before_request(app)
    get_prompt_on_startup()
    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")
    return app