import os
from bson import ObjectId
from pymongo import errors

from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for

from db import db
from decorator import check_token_expiry
from utils.jwt_utils import get_user_id, is_my_board

from scrap import scrap_image

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    board_list = list(boards.find({}).sort([("like_cnt", -1), ("comment_cnt", -1)]))
    for board in board_list:
        board['is_my_board'] = is_my_board(board['user_id'])
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
        tag = request.form.get('tag')
        subtag = request.form.get('subtag')
        image_url = scrap_image(url)

        error = None
        if not title :
            error = '제목을 입력하세요'
        elif not url :
            error = '링크를 입력하세요'
        elif not text :
            error = '내용을 입력하세요'
        elif not tag :
            error = '태그를 입력하세요'

        if image_url == None:
            image_url = "https://kraftonjungle.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F687a8a30-f3e6-4780-8e2c-a390011e3970%2F%25ED%2581%25AC%25EB%259E%2598%25ED%2594%2584%25ED%2586%25A4%25EC%25A0%2595%25EA%25B8%2580%25EB%25A1%259C%25EA%25B3%25A0.png?table=block&id=94d6df8c-7e1a-47af-871d-e52209f7d65c&spaceId=fb27bd18-c7e6-4eea-a450-a3c60e705e8a&width=250&userId=&cache=v2"
        
        if error:
            return render_template('board-register.html', error=error)

        articles = {
            'user_id': user_id,
            "image_url" : image_url,
            'title': title,
            'url': url,
            'text': text,
            'tag': tag,
            'subtag': subtag,
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
    if request.method == 'GET':
        board = db.boards.find_one({'_id': ObjectId(board_id)})
        if not board:
            return "게시글이 존재하지 않습니다."
        return render_template("board-update.html", board_info=board)

    elif request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')
        text = request.form.get('text')
        tag = request.form.get('tag')
        subtag = request.form.get('subtag')

        if not title:
            error = '제목을 입력하세요'
            return render_template('board-update.html', error=error)
        elif not url:
            error = '링크를 입력하세요'
            return render_template('board-update.html', error=error)
        elif not text:
            error = '내용을 입력하세요'
            return render_template('board-update.html', error=error)
        elif not tag or not subtag:
            error = '태그를 입력하세요'
            return render_template('board-update.html', error=error)
        else:
            db.boards.update_one(
                {'_id': ObjectId(board_id)},
                {'$set': {
                    'title': title,
                    'url': url,
                    'text': text,
                    'tag': tag,
                    'subtag': subtag
                }})
            return redirect('/')

@board_blueprint.route('/delete', methods=['POST'])
@check_token_expiry
def delete():
    board_id = request.form.get('board_id')

    board = boards.find_one({'_id': ObjectId(board_id)})
    if board:
        boards.delete_one({'_id': ObjectId(board_id)})
        return redirect('/')
    else:
        return "해당 게시글을 삭제할 수 있는 권한이 없습니다.", 403  # 403 Forbidden 에러 반환




