from fastapi import FastAPI
from app.api.routers import transactions, statistics
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title="Transaction Analysis Service", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(statistics.router)

# /docs будет доступно для Swagger UI
