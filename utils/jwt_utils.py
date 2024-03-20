import jwt
from flask import request, jsonify
from flask_jwt_extended import decode_token


def get_user_id():
    token = request.cookies.get('access_token')
    if not token:
        return None

    try:
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        return user_id

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


def is_my_board(board_user_id):
    token = request.cookies.get('access_token')
    if not token:
        return False

    try:
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        if user_id == board_user_id:
            return True

    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False