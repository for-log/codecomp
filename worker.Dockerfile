FROM python:3.12-slim
RUN pip install poetry

RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN poetry install
RUN sh
CMD ["poetry", "run", "faststream", "run", "worker_main:app", "--workers", "5"]