from db import db
from db.keywords_db import data

def get_keywords():
    keywords_dict = {}
    keywords = db["keywords"]
    keywords.delete_many({})
    for key, value in data.items():
        keywords.insert_one({**value, "key": key})
    cursor = keywords.find({}, {"key": 1, "_id": 0})
    keys = [doc["key"] for doc in cursor]
    for key in keys:
        keywords_dict[key] = get_tags(key)

    return keywords_dict

def get_tags(key):
    keywords = db["keywords"]
    keys = list(keywords.find({"key": key}))
    tags = [{"tags": doc["tags"]} for doc in keys][0]["tags"]
    
    return tags

keywords = get_keywords()