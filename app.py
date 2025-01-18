from flask import Flask
from auth.controller import auth_bp

from dotenv import load_dotenv
load_dotenv()
from ai.prompt import get_prompt_on_startup

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')

get_prompt_on_startup()

if __name__ == '__main__':
    app.run()