from sqlalchemy.orm import Session
from app.db.models import Transaction
from app.schemas import TransactionIn

def create_transaction(db: Session, data: TransactionIn):
    new_t = Transaction(
        transaction_id=data.transaction_id,
        user_id=data.user_id,
        amount=data.amount,
        currency=data.currency,
        timestamp=data.timestamp
    )
    db.add(new_t)

def delete_all_transactions(db: Session):
    db.query(Transaction).delete()
