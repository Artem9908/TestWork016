TestWork016

Запуск локально (без Docker)

Установить зависимости:
pip install -r requirements.txt
Поднять PostgreSQL и Redis локально или указать свои настройки в переменных окружения:
export DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/dbname
export REDIS_URL=redis://localhost:6379/0
export API_KEY=secret_api_key
Применить миграции:
alembic upgrade head
Запустить сервер:
uvicorn app.main:app --host 0.0.0.0 --port 8000
Запустить Celery воркер в другом терминале:
celery -A app.core.celery_app.celery_app worker --loglevel=INFO
После этого приложение будет доступно по адресу http://localhost:8000/docs.

Запуск с помощью Docker Compose

Собрать и запустить контейнеры:
docker-compose up --build
Это запустит сервисы db, redis, web и celery_worker.
После запуска сервисов, примените миграции:
docker-compose run web alembic upgrade head
Приложение будет доступно по адресу http://localhost:8000/docs.
Не забудьте использовать заголовок авторизации при запросах:
Authorization: ApiKey secret_api_key

Тестирование

Запустить тесты можно командой:

pytest
