from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class TransactionIn(BaseModel):
    transaction_id: str = Field(..., example="123456")
    user_id: str = Field(..., example="user_001")
    amount: float = Field(..., example=150.50)
    currency: str = Field(..., example="USD")
    timestamp: datetime

class TransactionOut(BaseModel):
    message: str
    task_id: str

class TopTransaction(BaseModel):
    transaction_id: str
    amount: float

class StatisticsOut(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: List[TopTransaction]
