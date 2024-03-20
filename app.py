import os

from dotenv import load_dotenv
from flask import Flask, redirect, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity

from api.board import board_blueprint
from api.comment import comment_blueprint
from api.user import user_blueprint
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

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = SECRET_KEY

@app.route('/refresh', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)