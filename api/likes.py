import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, redirect, request

from db import db
from utils.jwt_utils import get_user_id

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

likes_blueprint = Blueprint('likes', __name__)

users = db["users"]
boards = db["boards"]
comments = db["comments"]  
likes = db["likes"]

@likes_blueprint.route('/like', methods = ['POST'])
def like():
    board_id = request.form.get('board_id')
    board_info = boards.find_one({'_id': ObjectId(board_id)})

    user_id = get_user_id()

    if not user_id:
        return redirect('/login')

    
    if board_info['liked_users'] and user_id in board_info['liked_users']:
        new_like_cnt = board_info['like_cnt'] - 1
        liked_users = board_info['liked_users'].remove(user_id)
        db.boards.update_one(
            {'_id': ObjectId(board_id)},
            {'$set': {
                'like_cnt' : new_like_cnt,
                'liked_users': liked_users
            }}
        )
    else:
        new_like_cnt = board_info['like_cnt'] + 1
        liked_users = []
        liked_users.append(board_info['liked_users'])
        liked_users.append(user_id)
        db.boards.update_one(
            {'_id': ObjectId(board_id)},
            {'$set': {
                'like_cnt' : new_like_cnt,
                'liked_users': liked_users
            }}
        )

    previous_url = request.referrer
    domain_url = request.base_url.replace("like", "")
    if previous_url == domain_url:
        return redirect('/')
    else:
        return redirect('/board/' + board_id)

