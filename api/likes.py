import os

from bson import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, render_template, redirect, request, url_for, jsonify

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
    # 1. board_id : 어떤 게시물이 좋아요가 눌렀는가?
    board_id = request.form.get('board_id')
    
    board_info = boards.find_one({'_id': ObjectId(board_id)})
    # 2. user_id : 누가 눌렸냐?
    user_id = get_user_id()
    
    if user_id in board_info['liked_users'] :
        new_like_cnt = board_info['like_cnt'] - 1
        liked_users = board_info['liked_users']
        liked_users.remove(user_id)
        db.boards.update_one(
            {'_id': ObjectId(board_id)},
            {'$set': {
                'like_cnt' : new_like_cnt,
                'liked_users' : liked_users
            }}
        )
    else:
        new_like_cnt = board_info['like_cnt'] + 1
        liked_users = board_info['liked_users']
        liked_users.append(user_id)
        db.boards.update_one(
            {'_id': ObjectId(board_id)},
            {'$set': {
                'like_cnt' : new_like_cnt,
                'liked_users' : liked_users
            }}
        )
        
    
    return redirect('/board/' + board_id)