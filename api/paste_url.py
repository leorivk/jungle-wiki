import os
import clipboard
from bson import ObjectId
from dotenv import load_dotenv
from flask import Blueprint, render_template, redirect, request, url_for, jsonify

from db import db
from utils.jwt_utils import get_user_id

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

paste_blueprint = Blueprint('paste_url', __name__)

users = db["users"]
boards = db["boards"]
comments = db["comments"]  
likes = db["likes"]

@paste_blueprint.route('/paste', methods = ['GET'])
def paste():
    board_id = request.args.get('board_id')
    board_info = boards.find_one({'_id': ObjectId(board_id)})
    url = board_info['url']
    clipboard.copy(url)

    previous_url = request.referrer
    domain_url = request.base_url.replace("paste", "")
    if previous_url == domain_url:
        return redirect('/')
    else:
        return redirect('/board/' + board_id)