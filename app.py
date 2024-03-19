import os
from flask import Flask
from api.user import user_blueprint
from api.board import board_blueprint
from api.keywords import keyword_blueprint
from dotenv import load_dotenv
print("Done")
from scrap.json_provider import CustomJSONProvider

# .env 파일로부터 환경 변수 로드
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)
app.json = CustomJSONProvider(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(keyword_blueprint)

if __name__ == '__main__':
    app.run(debug=True)