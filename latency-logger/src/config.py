from pydantic_settings import BaseSettings

class Config(BaseSettings):
    kafka_broker_address: str = "localhost:19092"
    kafka_topic: str = "transaction_with_fraud_score"
    kafka_consumer_group: str = 'transaction_with_fraud_score_consumer_group'

config = Config()