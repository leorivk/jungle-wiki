from flask import Blueprint
from db import db

keyword_blueprint = Blueprint('keyword', __name__)

@keyword_blueprint.route("/keywords")
def get_keywords():
    keywords = db["keywords"]

    list = keywords.find({"_id": False, "order": False}).sort([("order", 1)])

    return list
    
