from flask import Flask
from auth.controller import auth_bp

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run()