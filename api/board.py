from flask import Blueprint, render_template, request, jsonify, redirect
from bson import ObjectId

from api.keywords import get_keywords
from db import db
import jwt
from decorator import check_token_expiry

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
@check_token_expiry
def create_page():
    return render_template("board-register.html")

@board_blueprint.route('/detail', methods = ['GET'])
@check_token_expiry
def detail_page():
    return render_template("board-detail.html")



@board_blueprint.route('/create', methods = ['POST'])
@check_token_expiry
def create() :
    user_id = get_user_id()

    title = request.form.get('title')
    url = request.form.get('url')
    text = request.form.get('text')
    tag1 = request.form.get('tag1')
    tag2 = request.form.get('tag2')

    articles = {
        'user_id' : user_id,
        'title' : title,
        'url' : url,
        'text' : text,
        'tag1' : tag1,
        'tag2' : tag2,
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
    elif not tag1 :
        error = '태그를 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not tag2 :
        error = '태그를 입력하세요'
        return render_template('board-register.html', error = error, **articles)

    # if user_id is None :
    #     return redirect('/login')


    print("user_id : " + str(user_id))
    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag1 + " " + tag2)

    db.boards.insert_one(articles)
    return redirect('/')

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