from app.db.session import SessionLocal
from app.db.models import Transaction
from app.schemas import StatisticsOut, TopTransaction
import redis
import json
from app.core.config import settings
from sqlalchemy import func

r = redis.from_url(settings.REDIS_URL)

def get_statistics() -> StatisticsOut:
    stats_data = r.get("statistics")
    if stats_data:
        stats = json.loads(stats_data)
        return StatisticsOut(**stats)
    else:
        # Если кэша нет, считаем "на лету"
        db = SessionLocal()
        try:
            total = db.query(Transaction).count()
            if total == 0:
                return StatisticsOut(total_transactions=0, average_transaction_amount=0, top_transactions=[])

            average = db.query(func.avg(Transaction.amount)).scalar()
            top = db.query(Transaction).order_by(Transaction.amount.desc()).limit(3).all()
            top_list = [TopTransaction(transaction_id=t.transaction_id, amount=t.amount) for t in top]

            return StatisticsOut(
                total_transactions=total,
                average_transaction_amount=float(average),
                top_transactions=top_list
            )
        finally:
            db.close()
