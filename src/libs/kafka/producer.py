import json
import threading

from kafka import KafkaProducer

from src import app


class Producer(threading.Thread):
    def __init__(self, topic, value, key):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.producer = None
        self.url = app.config['KAFKA_URL']
        self.topic = topic
        self.value = value
        self.key = key

    daemon = True

    def stop(self):
        self.stop_event.set()

    def run(self):
        self.producer = KafkaProducer(bootstrap_servers=self.url, key_serializer=str.encode,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        while not self.stop_event.is_set():
            self.send(topic=self.topic, value=self.value, key=self.key)
            self.stop()

        self.producer.close()

    def connected(self):
        if not self.producer:
            return False
        return self.producer.bootstrap_connected()

    def send(self, **kwargs):
        self.producer.send(**kwargs)
