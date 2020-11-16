from .. import Producer


class Event:
    def __init__(self):
        pass

    @classmethod
    def generate_endpoint(cls, topic, value):
        return f"/{topic}/{str(value)}"

    @classmethod
    def send(cls, topic, value, key):
        producer = Producer(topic=topic, value=value, key=key)
        producer.start()
