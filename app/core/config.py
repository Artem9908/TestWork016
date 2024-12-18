import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost:5432/dbname")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    API_KEY = os.getenv("API_KEY", "secret_api_key")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

settings = Settings()
