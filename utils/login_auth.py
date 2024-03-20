from flask import request
import jwt

def is_logged_in():
    try:
        token = request.cookies.get('access_token')
        is_logged_in = token is not None
    except (RuntimeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        is_logged_in = False
    return is_logged_in