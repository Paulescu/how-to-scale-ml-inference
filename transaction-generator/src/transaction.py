from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class Transaction(BaseModel):
    id: str
    credit_card: str
    card_holder: str
    expiration_date: str
    amount: float
    transaction_timestamp_ms: int