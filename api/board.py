import os
from bson import ObjectId
from pymongo import errors

from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for

from db import db
from decorator import check_token_expiry
from utils.jwt_utils import get_user_id

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    # ######################### 테스트 끝나면 삭제
    # boards.delete_many({})
    # #########################
    board_list = boards.find({})
    return render_template("index.html", board_list=board_list)

@board_blueprint.route('/create', methods = ['GET', 'POST'])
@check_token_expiry
def create():
    if request.method == 'GET':
        return render_template("board-register.html")

    elif request.method == 'POST':
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
            "liked_users": [],
            "like_cnt": 0,
            "comment_cnt": 0
        }

        try:
            boards.insert_one(articles)
        except errors.DuplicateKeyError:
            print("Duplicate user_id. Can't insert the article.")
        except Exception as e:
            print(f"An error occurred: {e}")

        board_id = boards["_id"]
        return redirect(url_for('board.home', board_id = board_id))


@board_blueprint.route('/update/<string:board_id>', methods=['GET', 'POST'])
@check_token_expiry
def update(board_id):
    user_id = get_user_id()

    if request.method == 'GET':
        board = db.boards.find_one({'_id': ObjectId(board_id)})
        if not board:
            return "게시글이 존재하지 않습니다."
        return render_template("board-update.html", board_info=board)

    elif request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')
        text = request.form.get('text')
        tag1 = request.form.get('tag1')
        tag2 = request.form.get('tag2')

        articles = {
            'user_id': user_id,
            'title': title,
            'url': url,
            'text': text,
            'tag1': tag1,
            'tag2': tag2,
            "likes": []
        }

        if not title:
            error = '제목을 입력하세요'
            return render_template('board-update.html', error=error, **articles)
        elif not url:
            error = '링크를 입력하세요'
            return render_template('board-update.html', error=error, **articles)
        elif not text:
            error = '내용을 입력하세요'
            return render_template('board-update.html', error=error, **articles)
        elif not tag1 or not tag2:
            error = '태그를 입력하세요'
            return render_template('board-update.html', error=error, **articles)
        else:
            db.boards.update_one(
                {'_id': ObjectId(board_id)},
                {'$set': {
                    'title': title,
                    'url': url,
                    'text': text,
                    'tag1': tag1,
                    'tag2': tag2
                }})
            return redirect('/')

@board_blueprint.route('/delete/<string:board_id>', methods=['POST'])
@check_token_expiry
def delete(board_id):
    user_id = get_user_id()

    board = db.boards.find_one({'_id': ObjectId(board_id), 'user_id': user_id})
    if board:
        db.boards.delete_one({'_id': ObjectId(board_id)})
        return redirect('/')
    else:
        return "해당 게시글을 삭제할 수 있는 권한이 없습니다.", 403  # 403 Forbidden 에러 반환




