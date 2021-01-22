import logging

from .events import *


def new_event_listener(event):
    topic = event.topic
    key = event.key
    data = event.value

    if topic == 'members':
        try:
            Member().handle_event(key=key, data=data)
        except:
            logging.error('Member event err')
