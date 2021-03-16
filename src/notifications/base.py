from src.common import Event


class Base:
    def __init__(self, key, data):
        self.topic = 'auth'
        self.event = Event()
        self.key = key
        self.data = data

    def dump(self):
        return self.topic, self.key, self.data

    def notify(self):
        self.event.send(topic=self.topic, key=self.key, value=self.data)
