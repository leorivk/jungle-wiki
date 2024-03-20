from flask import Blueprint, render_template, request, jsonify
from db import db
import jwt
from decorator import check_token_expiry

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

comment_blueprint = Blueprint('comment', __name__)

comments = db["comments"]