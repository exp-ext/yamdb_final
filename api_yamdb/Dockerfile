FROM python:3.7-slim

COPY ../ /app

WORKDIR /app/api_yamdb/

RUN pip install --upgrade pip && \
    pip install -r /app/api_yamdb/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0.0.0.0:8000" ]
