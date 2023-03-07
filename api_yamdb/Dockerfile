FROM python:3.7-slim

COPY . /app

WORKDIR /app/api_yamdb

RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
