from flask import Flask,jsonify
from auth.controller import authenticate_request
from users.controller import users_bp

from dotenv import load_dotenv
load_dotenv()
from ai.prompt import get_prompt_on_startup

app = Flask(__name__)

@app.before_request
def before_request():
    try:
        authenticate_request()
    except Exception as e:
        return jsonify({"error": str(e)}), 401
app.register_blueprint(users_bp, url_prefix='/users')

get_prompt_on_startup()

if __name__ == '__main__':
    app.run(debug=True)
