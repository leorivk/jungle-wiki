from flask import Blueprint, render_template, request, jsonify
from db import db
import jwt

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    return render_template("index.html")

@board_blueprint.route('/create', methods = ['GET'])
def create_page():
    return render_template("board-register.html")

@board_blueprint.route('/detail', methods = ['GET'])
def detail_page():
    return render_template("board-detail.html")

@board_blueprint.route('/update', methods = ['GET'])
def update_page():
    return render_template("board-update.html")

@board_blueprint.route('/create', methods = ['POST'])
def create() :
    user_id = get_user_id()

    title = request.form.get('title')
    if not title :
        return jsonify ({'error' : '제목이 없습니다.'}), 400

    url = request.form.get('url')
    if not url :
        return jsonify ({'error' : '링크가 없습니다.'}), 400

    text = request.form.get('text')
    if not url :
        return jsonify ({'error' : '내용이 없습니다.'}), 400

    tag = request.form.get('tag')
    if not url :
        return jsonify ({'error' : '태그가 없습니다.'}), 400

    articles = {
        'user_id' : user_id,
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
        "likes" : [

        ]
    }

    print("user_id : " + user_id)
    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag)

    db.articles.insert_one(articles)
    return jsonify({"message" : "Success"})


@board_blueprint.route('/read', methods = ['GET'])
def read () :
    board_list = list(boards.find({}, {'_id' : 0}))
    return jsonify ({'boards' : board_list})


@board_blueprint.route('/update/', methods = ['POST'])
def update () :

    title = request.form.get('title')
    if not title :
        return jsonify ({'error' : '제목이 없습니다.'}), 400

    url = request.form.get('url')
    if not url :
        return jsonify ({'error' : '링크가 없습니다.'}), 400

    text = request.form.get('text')
    if not url :
        return jsonify ({'error' : '내용이 없습니다.'}), 400

    tag = request.form.get('tag')
    if not url :
        return jsonify ({'error' : '태그가 없습니다.'}), 400

    articles = {
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
    }

    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag)

    db.articles.update_one(articles)
    return jsonify({"message" : "Success"})

@board_blueprint.route('/delete', methods = ['POST'])
def delete() :
    title = request.form.get('title')
    db.articles.delete_one({'title' : title})


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