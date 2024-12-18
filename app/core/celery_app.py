from celery import Celery
from app.core.config import settings

celery_app = Celery("tasks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

@celery_app.task(name="tasks.update_statistics")
def update_statistics():
    from sqlalchemy import func
    from app.db.session import SessionLocal
    from app.db.models import Transaction
    import heapq
    import json
    import redis
    from app.core.config import settings

    r = redis.from_url(settings.REDIS_URL)

    db = SessionLocal()
    try:
        total = db.query(Transaction).count()
        if total == 0:
            stats = {
                "total_transactions": 0,
                "average_transaction_amount": 0,
                "top_transactions": []
            }
            r.set("statistics", json.dumps(stats))
            return

        average = db.query(func.avg(Transaction.amount)).scalar()
        transactions = db.query(Transaction.transaction_id, Transaction.amount).all()

        # Находим топ-3 с помощью кучи (min-heap)
        heap = []
        for t_id, amt in transactions:
            if len(heap) < 3:
                heapq.heappush(heap, (amt, t_id))
            else:
                if amt > heap[0][0]:
                    heapq.heapreplace(heap, (amt, t_id))

        top_sorted = sorted(heap, key=lambda x: x[0], reverse=True)
        top_transactions = [
            {"transaction_id": t_id, "amount": amt}
            for amt, t_id in top_sorted
        ]

        stats = {
            "total_transactions": total,
            "average_transaction_amount": float(average),
            "top_transactions": top_transactions
        }

        r.set("statistics", json.dumps(stats))
    finally:
        db.close()
