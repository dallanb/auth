import json

import pytest
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

from src import app, Consumer, new_event_listener
from tests.helpers import new_event_listener as test_event_listener


@pytest.fixture(scope='session')
def kafka_conn():
    consumer = Consumer(topics=app.config['KAFKA_TOPICS'], event_listener=new_event_listener)
    consumer.start()


@pytest.fixture
def kafka_conn_last_msg():
    def _method(topic):
        consumer = KafkaConsumer(bootstrap_servers=app.config['KAFKA_URL'], group_id='testing',
                                 key_deserializer=bytes.decode,
                                 value_deserializer=lambda v: json.loads(v.decode('utf-8')), auto_offset_reset='latest',
                                 enable_auto_commit=False)

        partition = TopicPartition(topic, 0)
        consumer.assign([partition])
        last_pos = consumer.end_offsets([partition])
        pos = last_pos[partition]
        offset = OffsetAndMetadata(pos - 1, b'')
        consumer.commit(offsets={partition: offset})
        msg = next(consumer)
        consumer.close()
        return msg

    return _method


@pytest.fixture(scope='module')
def kafka_conn_custom_topics():
    def _method(topics):
        consumer = Consumer(topics=topics, event_listener=test_event_listener)
        consumer.start()

    return _method
