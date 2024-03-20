import datetime
import os
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import request, render_template, redirect
from flask_jwt_extended import decode_token

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

def check_token_expiry(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('access_token')
        if token:
            try:
                payload = decode_token(token)
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
