import time
from faker import Faker
from loguru import logger
from quixstreams import Application
# from threading import Lock

from src.transaction import Transaction
from src.config import config

shared_data = {'n_transactions_per_second': config.n_transactions_per_second}
# n_transactions_per_second = 100
# shared_data_lock = Lock()


def generate_transaction(fake) -> Transaction:
    """
    Generate a fake transaction using Faker
    """
    return Transaction(
        id=fake.uuid4(),
        credit_card=fake.credit_card_number(),
        card_holder=fake.name(),
        expiration_date=fake.future_date().strftime("%Y-%m-%d %H:%M:%S"),
        amount=fake.pyfloat(left_digits=4, right_digits=2, positive=True),
        transaction_timestamp_ms=int(time.time() * 1000),
    )

def produce_transactions():
    """
    Produce transactions to a Kafka topic at a rate given by 
    shared_data['n_transactions_per_second']

    This variable shared_data is shared between the Streamlit frontend (main process)
    and the producer (background thread) using a global variable.
    """    
    app = Application(broker_address=config.kafka_broker_address)
    topic = app.topic(name=config.kafka_topic, value_serializer='json')

    # we will use Faker to generate fake data    
    fake = Faker()
    
    with app.get_producer() as producer:
    
        while True:

            transactions = [generate_transaction(fake)
                            for _ in range(shared_data['n_transactions_per_second'])]

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

            logger.debug(f"Produced {len(transactions)} transactions to {config.kafka_topic} topic")

            time.sleep(1)

if __name__ == "__main__":

    try:
        produce_transactions()
    except KeyboardInterrupt:
        logger.info('Shutting down transaction generator...')