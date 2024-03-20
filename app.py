import os
from flask import Flask, redirect, request, make_response, render_template
from api.user import user_blueprint
from api.board import board_blueprint
from dotenv import load_dotenv
from scrap.json_provider import CustomJSONProvider
from flask_jwt_extended import JWTManager

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from api.keywords import get_keywords


# .env 파일로부터 환경 변수 로드
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)

app.json = CustomJSONProvider(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(board_blueprint)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = SECRET_KEY

print(get_keywords())

# @app.context_processor
# def inject_keywords():
#     keywords = get_keywords()
#     return render_template('sidebar.html', keywords=keywords)

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
        
if __name__ == '__main__':
    app.run(debug=True)