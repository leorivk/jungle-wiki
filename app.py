import os

from dotenv import load_dotenv
from flask import Flask, redirect, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity

from api.board import board_blueprint
from api.comment import comment_blueprint
from api.user import user_blueprint
from api.search import search_blueprint
from scrap.json_provider import CustomJSONProvider
from utils.keywords import keywords

# .env 파일로부터 환경 변수 로드
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)

app.json = CustomJSONProvider(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(board_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(search_blueprint)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # 실제 환경에서는 보안을 위해 환경변수 등에서 관리
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # JWT를 쿠키에서 로드하기 위한 설정
app.config['JWT_COOKIE_SECURE'] = False  # 개발 환경에서는 False, 실제 배포 시에는 True로 설정
app.config['JWT_COOKIE_CSRF_PROTECT'] = True  # CSRF 보호 활성화 (기본값은 True)

jwt = JWTManager(app)

@app.route('/refresh', methods=['POST'])
@jwt
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return redirect("/logout")
    
    try:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)

        previous = request.referrer
        
        if previous is None:
            previous = "/"
        
        response = make_response(redirect(previous))
        response.set_cookie('user_token', new_token)
        
        return response
    except:
        return redirect("/")
        
@app.context_processor
def inject_keywords():
    return dict(keywords=keywords)

@app.context_processor
def inject_logged_in():
    try:
        token = request.cookies.get('access_token')
        is_logged_in = token is not None
    except (RuntimeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        is_logged_in = False
    
    print(is_logged_in)
    return dict(logged_in=is_logged_in)

if __name__ == '__main__':    app.run(debug=True)