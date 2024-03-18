from flask import Blueprint, render_template
from db import db

board_blueprint = Blueprint('board', __name__)

boards = db["boards"]

@board_blueprint.route("/")
def home():
    return render_template("index.html")

@board_blueprint.route('/like', methods=['POST'])
def like():
    return "Like"


