import time
from faker import Faker
from loguru import logger
from quixstreams import Application

from src.transaction import Transaction

def generate_transaction(fake) -> Transaction:
    """
    Generate a fake transaction using Faker
    """
    return Transaction(
        id=fake.uuid4(),
        credit_card=fake.credit_card_number(),
        card_holder=fake.name(),
        expiration_date=fake.future_date().strftime("%Y-%m-%d %H:%M:%S"),
        amount=fake.pyfloat(left_digits=4, right_digits=2, positive=True)
    )

def run(
    n_transactions_per_second: int,
    kafka_broker_address: str,
    kafka_topic: str,
):
    logger.debug(f'Starting transaction generator with {n_transactions_per_second=}')
    
    app = Application(broker_address=kafka_broker_address)
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # we will use Faker to generate fake data    
    fake = Faker()
    
    with app.get_producer() as producer:
    
        while True:
            transactions = [generate_transaction(fake) for _ in range(n_transactions_per_second)]

            for transaction in transactions:
                
                # Serialize the transaction object into a message
                message = topic.serialize(
                    key=transaction.id,
                    value=transaction.model_dump(),
                )

                # Produce the message to the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key,
                )

            logger.debug(f"Produced {len(transactions)} transactions to Kafka topic {kafka_topic}")

            time.sleep(1)

if __name__ == "__main__":

    from src.config import config
    try:
        run(
            n_transactions_per_second=config.n_transactions_per_second,
            kafka_broker_address=config.kafka_broker_address,
            kafka_topic=config.kafka_topic,
        )
    except KeyboardInterrupt:
        logger.info('Shutting down transaction generator...')