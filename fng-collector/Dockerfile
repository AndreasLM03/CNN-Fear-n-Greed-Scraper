FROM python:3.12-slim

WORKDIR /app

# Install only what is needed — no browser, no selenium, no playwright
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.py scraper.py storage.py main.py ./

# Container runs once and exits; no ENTRYPOINT loop, no cron inside
CMD ["python", "main.py"]
