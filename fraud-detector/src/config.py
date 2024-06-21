from pydantic_settings import BaseSettings

class Config(BaseSettings):
    kafka_broker_address: str = "localhost:19092"
    kafka_input_topic: str = "transaction"
    kafka_output_topic: str = "transaction_with_fraud_score"
    kafka_consumer_group: str = 'transaction_consumer_group'

    ml_model_latency_ms: int = 100

config = Config() 