from flask import g
from kafka import KafkaAdminClient
from kafka.admin import NewTopic


class Admin:
    def __init__(self):
        self.client = KafkaAdminClient(bootstrap_servers=g.config['KAFKA_URL'])

    def create_topics(self, topics):
        topics = [NewTopic(topic, 1, 1) for topic in topics]
        self.client.create_topics(new_topics=topics)

    def delete_topics(self, topics):
        self.client.delete_topics(topics=topics)
