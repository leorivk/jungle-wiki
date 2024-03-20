from flask import request, render_template, redirect
from functools import wraps
from dotenv import load_dotenv
import jwt
import datetime
import os

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

def check_token_expiry(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('user_token')
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                # 토큰의 유효 기간 확인
                expiration_date = datetime.datetime.fromtimestamp(payload['exp'])
                current_date = datetime.datetime.now()
                if current_date > expiration_date:
                    return redirect("/refresh")
            except jwt.ExpiredSignatureError:
                return redirect("/refresh")
            except jwt.InvalidTokenError:
                error_message = "토큰이 유효하지 않음"
                return render_template('login.html', error_message=error_message)
            
        return func(*args, **kwargs)
    return decorated_function
