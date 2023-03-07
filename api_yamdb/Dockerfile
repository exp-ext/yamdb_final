FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY api_yamdb api_yamdb

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
