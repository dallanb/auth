from http import HTTPStatus
from ..common.mail import Mail
from ..common.error import ManualException


def send_register_mail(user):
    try:
        mail = Mail()
        html = mail.generate_body('register', user=user)
        mail.send(
            to=user['email'],
            subject='Tech Tapir Registration',
            html=html
        )
    except Exception as e:
        raise ManualException(code=HTTPStatus.NOT_FOUND.value, msg=HTTPStatus.NOT_FOUND.phrase)
