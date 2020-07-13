import uuid
from time import time


def time_now():
    return int(time() * 1000.0)


def generate_uuid():
    return uuid.uuid4()


def get_jwt_part(token, index):
    return token.decode("utf-8").split(".")[index]
