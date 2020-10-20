import json
import multiprocessing

from kafka import KafkaConsumer


class Consumer(multiprocessing.Process):
    def __init__(self, url, topics, event_listener):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.url = url
        self.topics = topics
        self.event_listener = event_listener

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=self.url, key_deserializer=bytes.decode,
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')))
        consumer.subscribe(self.topics)

        while not self.stop_event.is_set():
            for event in consumer:
                self.event_listener(event=event)
                if self.stop_event.is_set():
                    break

        consumer.close()
