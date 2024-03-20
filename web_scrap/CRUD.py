from flask import Flask, render_template, jsonify, request, redirect
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["jg_wiki_db"]
collection = db['boards']

@app.route('/create', methods = ['POST'])
def create () :
    error = None
    title = request.form.get('title')
    url = request.form.get('url')
    text = request.form.get('text')
    tag = request.form.get('tag')
    
    articles = {
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
    }
    
    if not title :
        error = '제목을 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not url :
        error = '링크를 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not text :
        error = '내용을 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    elif not tag :
        error = '태그를 입력하세요'
        return render_template('board-register.html', error = error, **articles)
    
    
    
    db.collection.insert_one(articles)
    return render_template('board-register.html')
    

@app.route('/read', methods = ['GET'])
def read () :
    boards = list(collection.find({}, {'_id' : 0}))
    return redirect('/index.html')
    
    
@app.route('/update', methods = ['POST'])
def update () :
    title = request.form.get('title')
    url = request.form.get('url')
    text = request.form.get('text')
    tag = request.form.get('tag')
    
    
    if not title :
        error = '제목을 입력하세요'
        return render_template('board-update.html', error = error)
    elif not url :
        error = '링크를 입력하세요'
        return render_template('board-update.html', error = error)
    elif not text :
        error = '내용을 입력하세요'
        return render_template('board-update.html', error = error)
    elif not tag :
        error = '태그를 입력하세요'
        return render_template('board-update.html', error = error)
    
    
    articles = {
        'title' : title,
        'url' : url,
        'text' : text,
        'tag' : tag,
    }
    
    db.collection.insert_one(articles)
    return render_template('index.html')
    
@app.route('/delete', methods = ['POST'])
def delete() :
    title = request.form.get('title')
    db.collection.delete_one({'title' : title})
    return render_template('index_html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)