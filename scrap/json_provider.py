import json

from flask.json.provider import JSONProvider
from bson import ObjectId

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        print("ifsdafdf")
        if isinstance(o, ObjectId):
            print("deddd")
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        print("dumps")
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        print("loads")
        return json.loads(s, **kwargs)