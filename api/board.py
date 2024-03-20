import os
from pymongo import errors

from dotenv import load_dotenv
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from db import db
from decorator.decorator import check_token_expiry
from utils.jwt_utils import get_user_id

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    data = boards.find({})
    print(list(data))
    return render_template("index.html")

@board_blueprint.route('/create', methods = ['GET'])
@check_token_expiry
def create_page():
    return render_template("board-register.html")

@board_blueprint.route('/update', methods = ['GET'])
@check_token_expiry
def update_page():
    return render_template("board-update.html")

@board_blueprint.route('/create', methods = ['POST'])
@check_token_expiry
def create():
    user_id = get_user_id()

    title = request.form.get('title')
    url = request.form.get('url')
    text = request.form.get('text')
    tag = request.form.get('tag'),
    subtag = request.form.get('subtag')

    error = None
    if not title :
        error = '제목을 입력하세요'
    elif not url :
        error = '링크를 입력하세요'
    elif not text :
        error = '내용을 입력하세요'
    elif not tag :
        error = '태그를 입력하세요'

    if error:
        return render_template('board-register.html', error=error)

    articles = {
        'user_id': user_id,
        'title': title,
        'url': url,
        'text': text,
        'tag': tag,
        'subtag' : subtag,
        "likes": []
    }

    try:
        boards.insert_one(articles)
    except errors.DuplicateKeyError:
        print("Duplicate user_id. Can't insert the article.")
    except Exception as e:
        print(f"An error occurred: {e}")

    board_id = boards["_id"]
    return redirect(url_for('board.home', board_id = board_id))


@board_blueprint.route('/update', methods = ['POST'])
@check_token_expiry
def update() :

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


