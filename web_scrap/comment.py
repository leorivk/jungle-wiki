from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["jg_wiki_db"]
reply = db['boards']

@app.route('/comment', methods = ['POST'])
def create () :
    
    comment = request.form.get('comment')
    if not comment :
        return jsonify ({'error' : '댓글이 없습니다.'}), 400
    
    list = {
        'comment' : comment,
    }
    
    
    reply.insert_one(list)
    return jsonify({"message" : "Success"})
    


@app.route('/comment', methods = ['GET'])
def read () :
    comment = list(reply.find({}, {'_id' : 0}))
    return jsonify ({'comment' : comment})
    
    
@app.route('/comment/delete', methods = ['POST'])
def delete() :
    comment = request.form.get('comment')
    reply.delete_one({'comment' : comment})
    return jsonify({"message" : "Success"})
    
if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)