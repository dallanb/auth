import os
from flask import render_template
from ..external import Mailer


class Mail:
    def __init__(self):
        self.mailer = Mailer()

    def send(self, to, subject, html, text=None):
        self.mailer.send_mail(to=to, subject=subject, html=html, text=text)

    def generate_body(self, template, **kwargs):
        return render_template(
            self.get_filename(template),
            **kwargs
        )

    @staticmethod
    def get_filename(template):
        return os.path.join('email', f'{template}.html')
