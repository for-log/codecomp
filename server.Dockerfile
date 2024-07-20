FROM python:3.12-slim
RUN pip install poetry

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN poetry install
EXPOSE 8000
RUN sh
CMD ["poetry", "run", "gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]