import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, render_template, redirect, request

from db import db
from utils.jwt_utils import get_user_id

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

comment_blueprint = Blueprint('comment', __name__)

users = db["users"]
boards = db["boards"]
comments = db["comments"]

@comment_blueprint.route('/board/<string:board_id>', methods = ['GET'])
def board_detail_page(board_id):
    user_id = get_user_id()
    board_info = boards.find_one({'_id': ObjectId(board_id)})
    comment_list = list(comments.find({'board_id': board_id}))

    return render_template("board-detail.html", board_info = board_info, comment_list = comment_list, logged_user_id = user_id, board_id = board_id)

@comment_blueprint.route('/comment', methods = ['POST'])
def comment_create():
    user_id = get_user_id()
    user_info = users.find_one({'id': user_id})

    board_id = request.form.get('board_id')
    board_info = boards.find_one({'_id': ObjectId(board_id)})

    contents = request.form.get('contents')

    print(board_info['comment_cnt'])
    new_commnet_cnt = board_info['comment_cnt'] + 1
    boards.update_one({'_id': ObjectId(board_id)}, {'$set': {'comment_cnt': new_commnet_cnt}})

    comments.insert_one({
        'user_id': user_id,
        'user_name': user_info['username'],
        'board_id': board_id,
        'comment_contents': contents
    })

    return redirect('/board/' + board_id)

@comment_blueprint.route('/comment/delete', methods = ['POST'])
def comment_delete():
    board_id = request.form.get('board_id')

    comment_id = request.form.get('comment_id')
    comments.delete_one({'_id': ObjectId(comment_id)})

    return redirect('/board/' + board_id)