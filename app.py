import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from utils.auth import auth_blueprint
from utils.config import Config
from utils.context_processors import inject_template_globals

from api.board import board_blueprint
from api.comment import comment_blueprint
from api.likes import likes_blueprint
from api.paste_url import paste_blueprint
from api.search import search_blueprint
from api.user import user_blueprint

# .env 파일로부터 환경 변수 로드
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(likes_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(paste_blueprint)

app.context_processor(inject_template_globals)

if __name__ == '__main__':
    app.run(debug=True)