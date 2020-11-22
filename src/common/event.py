from ..libs import Producer


class Event:
    @classmethod
    def _generate_endpoint(cls, topic, value):
        return {
            'endpoint': f"/{topic}/{str(value)}"
        }

    @classmethod
    def send(cls, topic, value, key):
        producer = Producer(topic=topic, value=value, key=key)
        producer.start()
