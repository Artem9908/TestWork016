from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TransactionIn, TransactionOut
from app.db.session import SessionLocal
from app.api.security import verify_api_key
from app.services.transactions import create_transaction, delete_all_transactions
from app.core.celery_app import celery_app

router = APIRouter()

@router.post("/transactions", response_model=TransactionOut)
def post_transaction(data: TransactionIn, _=Depends(verify_api_key)):
    db = SessionLocal()
    try:
        create_transaction(db, data)
        db.commit()
        # Запуск задачи Celery на обновление статистики
        task = celery_app.send_task("tasks.update_statistics")
        return {"message": "Transaction received", "task_id": task.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.delete("/transactions")
def delete_transactions(_=Depends(verify_api_key)):
    db = SessionLocal()
    try:
        delete_all_transactions(db)
        db.commit()
        # Обновляем статистику (обнуление)
        celery_app.send_task("tasks.update_statistics")
        return {"message": "All transactions deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
