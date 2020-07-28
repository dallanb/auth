import json


def get_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except TypeError as e:
        return {}
