from flask import Blueprint, render_template, request, jsonify, redirect

from api.keywords import get_keywords
from db import db
import jwt
from decorator import check_token_expiry

from dotenv import load_dotenv
import os

from api.keywords import get_keywords

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    keywords = get_keywords()
    return render_template("index.html")

@board_blueprint.route('/create', methods = ['GET'])
@check_token_expiry
def create_page():
    return render_template("board-register.html")

@board_blueprint.route('/detail', methods = ['GET'])
@check_token_expiry
def detail_page():
    return render_template("board-detail.html")

@board_blueprint.route('/update', methods = ['GET'])
@check_token_expiry
def update_page():
    return render_template("board-update.html")

@board_blueprint.route('/create', methods = ['POST'])
@check_token_expiry
def create() :
    user_id = get_user_id()

    title = request.form.get('title')
    url = request.form.get('url')
    text = request.form.get('text')
    tag = request.form.get('tag')

    articles = {
        'user_id' : user_id,
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
        "likes" : [

        ]
    }


    if not title :
        error = '제목을 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not url :
        error = '링크를 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not text :
        error = '내용을 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not tag :
        error = '태그를 입력하세요'
        return render_template('board-register.html', error = error, **articles)

    # if user_id is None :
    #     return redirect('/login')


    print("user_id : " + str(user_id))
    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag)

    db.boards.insert_one(articles)
    return redirect('/')


@board_blueprint.route('/read', methods = ['GET'])
def read () :
    board_list = list(boards.find({}, {'_id' : 0}))
    return jsonify ({'boards' : board_list})


@board_blueprint.route('/update/', methods = ['POST'])
@check_token_expiry
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

    db.boards.update_one(articles)
    return jsonify({"message" : "Success"})

@board_blueprint.route('/delete', methods = ['POST'])
@check_token_expiry
def delete(board_id) :

    user_id = get_user_id()

    board = db.boards.find_one({'_id' : board_id, 'user_id' : user_id})
    if board :
        db.boards.delete_one({'_id' : board_id})
        return redirect('/')
    else:
        return redirect('/login')

    title = request.form.get('title')
    db.boards.delete_one({'title' : title})
    return redirect('/')


def get_user_id():
    token = request.cookies.get('user_token')

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401