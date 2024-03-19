from db import db

def get_keywords():
    keywords = db["keywords"]

    list = keywords.find({"_id": False, "order": False}).sort([("order", 1)])

    return list
    
