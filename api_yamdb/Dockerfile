FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0.0.0.0:8000"]
