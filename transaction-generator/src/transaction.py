from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class Transaction(BaseModel):
    id: str
    credit_card: str
    card_holder: str
    expiration_date: str
    amount: float
    timestamp_ms: int