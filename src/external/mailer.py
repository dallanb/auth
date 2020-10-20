import json
from flask import g

from . import Base


class Mailer(Base):
    def __init__(self):
        Base.__init__(self)
        self.base_url = g.config['MAILER_URL']

    # create a Kong consumer
    def send_mail(self, to, subject, html, text=None):
        url = f'{self.base_url}/send'
        data = {
            'data': json.dumps({
                'to': to,
                'subject': subject,
                'html': html,
                'text': text
            })
        }
        res = self.post(url=url, json=data)
        return res.json()
