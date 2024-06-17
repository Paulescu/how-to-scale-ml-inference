from pydantic_settings import BaseSettings

class Config(BaseSettings):
    kafka_broker_address: str = "localhost:19092"
    kafka_topic: str = "transaction"
    n_transactions_per_second: int = 100

config = Config()