FROM python:3.7-slim

COPY api_yamdb/requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt --no-cache-dir

COPY ../ /app

WORKDIR /app/api_yamdb/

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
