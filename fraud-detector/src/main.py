from loguru import logger
from quixstreams import Application

from src.predictor import MyModel

def run(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    ml_model_latency_ms: int,
):
    """
    This function
    - reads transactions from a Kafka topic
    - calculates the fraud score for each transaction, and
    - produces the transaction with the fraud score to another Kafka topic

    The fraud score is calculated using a Mocked ML model
    """
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        auto_offset_reset='latest',
    )
    
    # specify input and output topics for this application
    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # creating a streaming dataframe
    # to apply transformations on the incoming data
    sdf = app.dataframe(input_topic)

    ml_model = MyModel(latency_ms=ml_model_latency_ms)

    # generate the fraud score for each transaction
    sdf = sdf.apply(lambda value: {
        **value,
        'is_fraud': ml_model.predict(value)},
    )
    
    # import time
    # sdf['prediction_timestamp_ms'] = sdf.apply(
    #     lambda _: int(time.time() * 1000),
    # )

    sdf.update(logger.debug)

    # write the data to the output topic
    sdf = sdf.to_topic(output_topic)

    sdf = sdf.update(logger.debug)

    # We are done defining the streaming application. Now we need to run it.
    # Let's kick-off the streaming application
    app.run(sdf)


if __name__ == "__main__":

    from src.config import config
    try:
        run(
            kafka_broker_address=config.kafka_broker_address,
            kafka_input_topic=config.kafka_input_topic,
            kafka_output_topic=config.kafka_output_topic,
            kafka_consumer_group=config.kafka_consumer_group,
            ml_model_latency_ms=config.ml_model_latency_ms,
        )
    except KeyboardInterrupt:
        logger.info('Shutting down fraud detector...')