FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.2.1 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction

COPY src/fng-collector/ ./

# Container runs once and exits; no ENTRYPOINT loop, no cron inside
CMD ["python", "main.py"]
