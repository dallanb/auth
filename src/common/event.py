from ..libs import Producer


class Event:
    def __init__(self):
        pass

    @staticmethod
    def generate_endpoint(topic, value):
        return f"/{topic}/{str(value)}"

    @staticmethod
    def send(topic, value, key):
        producer = Producer(topic=topic, value=value, key=key)
        producer.start()
