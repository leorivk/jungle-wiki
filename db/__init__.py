from pymongo import MongoClient

client = MongoClient('mongodb://test:test@43.203.181.68', 27017)

db = client["jg_wiki_db"]