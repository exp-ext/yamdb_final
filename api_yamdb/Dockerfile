FROM python:3.7-slim

WORKDIR /app

COPY ./api_yamdb /app/api_yamdb

RUN pip install --no-cache-dir -r /app/api_yamdb/requirements.txt

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
