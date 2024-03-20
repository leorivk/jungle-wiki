from flask import request
from utils.keywords import keywords

import jwt

def inject_template_globals():
    try:
        token = request.cookies.get('access_token')
        is_logged_in = token is not None
    except (RuntimeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        is_logged_in = False
    
    return dict(keywords=keywords, logged_in=is_logged_in)