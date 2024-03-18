from flask import Flask, render_template

from api.user import user_blueprint
from api.board import board_blueprint
from dotenv import load_dotenv
import os


# .env 파일로부터 환경 변수 로드
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)

app.register_blueprint(user_blueprint)
app.register_blueprint(board_blueprint)

if __name__ == '__main__':
    app.run(debug=True)