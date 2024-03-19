from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from db import db
from scrap import scrap_tistory, scrap_velog

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/search', methods=['POST'])
def search():
    keyword = request.args.get('keyword')
    urls = db.users.find({}, {'_id': 0, 'name': 0, 'id': 0,'password': 0,'blog_url': 1})
    for url in urls:
        # 티스토리이면 ~
        scrap_tistory(url, keyword)
        # 벨로그이면 ~
        scrap_velog(url, keyword)
    
    # 그럼 키워드에 맞는 결과들이 db.blogs?에 저장
    # render_template 시 해당 데이터 전달


