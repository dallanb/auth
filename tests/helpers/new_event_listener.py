import logging

from src.events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value

    if topic == 'auth_test':
        try:
            Auth().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('Auth event err')
    if topic == 'members_test':
        try:
            Member().handle_event(key=key, data=data)
        except Exception as ex:
            logging.error(ex)
            logging.error('Member event err')
