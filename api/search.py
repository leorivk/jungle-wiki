from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db import db

search_blueprint = Blueprint('search', __name__)

boards = db["boards"]

@search_blueprint.route('/search', methods=['GET'])
def search():
    keyword = request.args.get("keyword")

    if not keyword:
        return jsonify({"error": "No query provided"}), 400

    regex_query = {'$regex': keyword, '$options': 'i'}  # 대소문자 무시를 위해 'i' 옵션 사용
    search_query = {
        '$or': [
            {'title': regex_query},
            {'text': regex_query},
            {'tag': regex_query}
        ]
    }

    search_results = list(boards.find(search_query, {'_id': 0}))

    return jsonify(search_results)
    