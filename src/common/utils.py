import uuid
from time import time


def time_now():
    return int(time() * 1000.0)


def generate_uuid():
    return uuid.uuid4()


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
