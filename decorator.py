from flask import request, redirect, url_for
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
                decoded_token = jwt.decode(token, SECRET_KEY)
                # 토큰의 유효 기간 확인
                expiration_date = datetime.datetime.fromtimestamp(decoded_token['exp'])
                current_date = datetime.datetime.now()
                if current_date > expiration_date:
                    # 토큰이 만료됨
                    print("토큰이 만료됨")
                    return redirect(url_for('logout'))
            except jwt.ExpiredSignatureError:
                # 토큰이 만료됨
                print("토큰이 만료됨")
                return redirect(url_for('logout'))
            except jwt.InvalidTokenError:
                # 토큰이 유효하지 않음
                print("토큰이 유효하지 않음")
                pass
        return func(*args, **kwargs)
    return decorated_function
