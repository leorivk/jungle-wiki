from db import db

def get_keywords():
    keywords = db["keywords"]
    print(list(keywords.find({}, {"order" : 0}).sort([("order", 1)])))

