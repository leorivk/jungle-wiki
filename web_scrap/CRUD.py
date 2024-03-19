from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["jg_wiki_db"]
collection = db['boards']

@app.route('/create', methods = ['POST'])
def create () :
    title = request.form.get('title')
    if not title :
        return jsonify ({'error' : '제목이 없습니다.'}), 400
    
    url = request.form.get('url')
    if not url :
        return jsonify ({'error' : '링크가 없습니다.'}), 400
    
    text = request.form.get('text')
    if not url :
        return jsonify ({'error' : '내용이 없습니다.'}), 400
    
    tag = request.form.get('tag')
    if not url :
        return jsonify ({'error' : '태그가 없습니다.'}), 400
    
    articles = {
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
    }
    
    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag)
    
    db.collection.insert_one(articles)
    return jsonify({"message" : "Success"})
    

@app.route('/read', methods = ['GET'])
def read () :
    boards = list(collection.find({}, {'_id' : 0}))
    return jsonify ({'boards' : boards})
    
    
@app.route('/update', methods = ['POST'])
def update () :
    title = request.form.get('title')
    if not title :
        return jsonify ({'error' : '제목이 없습니다.'}), 400
    
    url = request.form.get('url')
    if not url :
        return jsonify ({'error' : '링크가 없습니다.'}), 400
    
    text = request.form.get('text')
    if not text :
        return jsonify ({'error' : '내용이 없습니다.'}), 400
    
    tag = request.form.get('tag')
    if not tag :
        return jsonify ({'error' : '태그가 없습니다.'}), 400
    
    articles = {
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
    }
    
    print("title : " + title)
    print("url : " + url)
    print("text : " + text)
    print("tag : " + tag)
    
    db.collection.update_one(articles)
    return jsonify({"message" : "Success"})
    
@app.route('/delete', methods = ['POST'])
def delete() :
    title = request.form.get('title')
    db.collection.delete_one({'title' : title})
    
if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)