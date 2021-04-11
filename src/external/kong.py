from . import Base
from .. import app


class Kong(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = app.config['KONG_URL']
        self.api_key = app.config['KONG_API_KEY']
        self.secret = app.config['SECRET_KEY']

    def url(self, endpoint):
        full_url = f'{self.base_url}/{endpoint}'
        if self.api_key:
            full_url += f'apikey={self.api_key}'
        return full_url

    # create a Kong consumer
    def create_consumer(self, uuid, username):
        url = self.url(endpoint='consumers')
        json = {
            'username': username,
            'custom_id': uuid
        }
        res = self.post(url=url, json=json)
        return res.json()

    # create jwt credential with Kong
    def create_jwt_credential(self, username, key, algorithm="HS256"):
        url = self.url(endpoint=f'consumers/{username}/jwt')
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        data = {
            "key": key,
            "algorithm": algorithm,
            "secret": self.secret
        }
        res = self.post(url=url, data=data, headers=headers)
        return res.json()

    # delete jwt credential with Kong
    def delete_jwt_credential(self, username, jwt_id):
        url = self.url(endpoint=f'consumers/{username}/jwt/{jwt_id}')
        res = self.delete(url=url)
        return res
