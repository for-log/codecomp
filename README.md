# Платформа для публикации и решения задач по программированию (В разработке...)
# TODO:
- [x] Backend
- [ ] Frontend
- [ ] Dockerfile
# Stack:
- Postgresql
- Redis
- RabbitMQ
# Env:
- POSTGRES_URL - Подключение к postgresql
- REDIS_URL - Подключение к redis
- RABBIT_URL - Подключение к rabbitmq
# Запуск сервера:
```
poetry install
poetry run fastapi dev main.py
```
# Запуск воркера:
```
poetry install
poetry run faststream run worker:app
```