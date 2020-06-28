import json


def create_message(message):
    return {'type': 'success', 'message': message}


def create_error(message):
    return {'type': 'danger', 'message': message}


def get_json(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except TypeError as e:
        return {}
