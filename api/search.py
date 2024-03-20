from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db import db
from pymongo.errors import PyMongoError  # MongoDB 에러 핸들링을 위해 추가

search_blueprint = Blueprint('search', __name__)

boards = db["boards"]

@search_blueprint.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')  # 쿼리 파라미터에서 'keyword' 값을 가져옴
    print(keyword)
    if not keyword:
        return render_template("index.html", error_message="검색어를 입력해주세요.")

    regex_query = {'$regex': keyword, '$options': 'i'}  # 대소문자 무시를 위해 'i' 옵션 사용
    search_query = {
        '$or': [
            {'title': regex_query},
            {'text': regex_query},
            {'tag': regex_query}
        ]
    }

    try:
        board_list = boards.find(search_query)
    except PyMongoError as e:
        # MongoDB에서 발생한 에러를 로깅하고, 사용자에게 에러 메시지를 반환
        print(f"Error accessing database: {e}")  # 로깅, 실제 애플리케이션에서는 logging 모듈 사용을 고려
        return jsonify({"error": "Database access failed"}), 500

    print("SUCCESS")
    return render_template("index.html", board_list = board_list)
    