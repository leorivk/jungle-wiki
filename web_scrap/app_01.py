import requests
from bson import ObjectId
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


app.json = CustomJSONProvider(app)

@app.route('/')
def home():
   return 


@app.route('/search')
def search() :
    keyword = request.args.get('keyword')
    username = request.args.get('usrername')
    data = requests.get(url_receive, headers=headers)
    

@app.route('POST')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   
   
