from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db import db

import jwt
import bcrypt
import datetime

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

user_blueprint = Blueprint('user', __name__)

users = db["users"]

@user_blueprint.route('/join', methods=['GET'])
def join_page():
    return render_template('join.html')

@user_blueprint.route('/join', methods=['POST'])
def join():
    data = request.form
    required_fields = ['username', '_id', 'password', 'blog_url']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Name, ID, Password, and Blog URL are required"}), 400

    if users.find_one({"id": data['_id']}):
        return jsonify({"message": "User ID already exists"}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    users.insert_one({
        "username": data['username'],
        "id": data['_id'],
        "password": hashed_password,
        "blog_url": data['blog_url']
    })

    return redirect(url_for('user.login_page'))

@user_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.form

    required_fields = ['_id', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "ID and Password are required"}), 400

    user = users.find_one({"id": data['_id']})
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid ID or password"}), 401

    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, SECRET_KEY)

    return jsonify({"token": token}), 200

def get_user_id():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"message": "Authorization token is missing"}), 401

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401