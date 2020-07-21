from flask import g

from . import Base


class Kong(Base):
    def __init__(self):
        Base.__init__(self)
        self.host = g.config['KONG_HOST']
        self.port = g.config['KONG_PORT']
        self.base_url = f'http://{self.host}:{self.port}'
        self.secret = g.config['SECRET_KEY']

    # create a Kong consumer
    def create_consumer(self, uuid, username):
        url = f'{self.base_url}/consumers'
        json = {
            'username': username,
            'custom_id': uuid
        }
        res = self.post(url=url, json=json)
        return res.json()

    # create jwt credential with Kong
    def create_jwt_credential(self, username, key, algorithm="HS256"):
        url = f'{self.base_url}/consumers/{username}/jwt'
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
        url = f'{self.base_url}/consumers/{username}/jwt/{jwt_id}'
        res = self.delete(url=url)
        return res
