from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client["jg_wiki_db"]

print(db)