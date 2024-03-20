from db import db

def get_keywords():
    keywords = db["keywords"]
    return list(keywords.find({}, {"_id" : 0, "order" : 0}).sort([("order", 1)]))

