from flask import Blueprint, jsonify, request, render_template, redirect, url_for, make_response
from db import db
from flask_jwt_extended import create_access_token, create_refresh_token

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
    return render_template("login.html")


@user_blueprint.route('/login', methods=['POST'])
def login():
    id = request.form.get('_id', '')
    password = request.form.get('password', '')

    if not password:
        return redirect(url_for('user.login', _id=id, error_message='비밀번호를 입력하세요'))
    
    if not id:
        return redirect(url_for('user.login', error_message='아이디를 입력하세요'))

    user = users.find_one({"id": id})
    if not user:
        return redirect(url_for('user.login', error_message='존재하지 않는 ID입니다.'))
    access_token = create_access_token(identity=user["_id"])
    refresh_token = create_refresh_token(identity=user["_id"])
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return render_template('login.html', error_message='잘못된 비밀번호 입니다.')

    response = make_response(render_template("index.html", logged_in = True))
    response.set_cookie('access_token', access_token)
    response.set_cookie('refresh_token', refresh_token)

    return response

@user_blueprint.route("/logout")
def logout():
    response = make_response(render_template("index.html", logged_in=False))
    response.set_cookie('user_token', '', expires=0)
    return redirect("/")
