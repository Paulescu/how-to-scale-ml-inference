from loguru import logger
from quixstreams import Application
import json
import time

from prometheus_client import start_http_server, Summary

def run(
    kafka_topic: str,
    kafka_broker_address: str,
    kafka_consumer_group: str,
) -> None:
    """
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset="latest"
    )

    # buffer = []
    start_http_server(8000)
    s = Summary('ml_pipeline_latency_ms',
                'Milliseconds elapsed between the transaction timestamp and the \
                 timestamp when the prediction is ready to be served')

    # Create a consumer and start a polling loop
    with app.get_consumer() as consumer:
        consumer.subscribe(topics=[kafka_topic])

        while True:
            msg = consumer.poll(1)

            if msg is None:
                logger.error('No message received from Kafka topic')
                continue

            elif (msg is not None) and (msg.error() is not None):
                logger.error(f'Error while consuming message: {msg.error()}')
                continue
            
            else:
                # we have a message without an error. Let's process it!
            
                # decode the binary message into a dictionary
                msg = json.loads(msg.value().decode('utf-8'))

                # compute the latency in ms between the timestamp of the message and the
                # current time
                current_timestamps_ms = int(time.time() * 1000)
                latency_ms = current_timestamps_ms - msg['transaction_timestamp_ms']

                s.observe(latency_ms)
                # breakpoint()

                logger.debug(f'Latency: {latency_ms} ms')

if __name__ == '__main__':

    from src.config import config
    logger.debug(config.model_dump())

    try:
        run(
            kafka_topic=config.kafka_topic,
            kafka_broker_address=config.kafka_broker_address,
            kafka_consumer_group=config.kafka_consumer_group,
        )
    except KeyboardInterrupt:
        logger.info('Exiting neatly!')