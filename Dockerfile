
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --retries 5 --timeout 30 \
    -r requirements.txt

COPY app/ ./
COPY db/schema.sql /db/schema.sql

EXPOSE 5000

CMD ["sh", "-c", "python -c 'from app import initialize_database; initialize_database()' && exec gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile - app:app"]
