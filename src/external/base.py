import requests
import logging


class Base:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def get(**kwargs):
        url = kwargs.get('url', None)
        headers = kwargs.get('headers', None)
        return requests.get(url, headers)

    @staticmethod
    def post(**kwargs):
        url = kwargs.get('url', None)
        data = kwargs.get('data', None)
        json = kwargs.get('json', None)
        files = kwargs.get('files', None)
        headers = kwargs.get('headers', None)
        return requests.post(url, data=data, json=json, files=files, headers=headers)

    @staticmethod
    def delete(**kwargs):
        url = kwargs.get('url', None)
        headers = kwargs.get('headers', None)
        return requests.delete(url, headers=headers)
