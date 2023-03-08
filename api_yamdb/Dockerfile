FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
        gcc \
        cmake \
        libpq-dev \
        python3-dev \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "--chdir", "api_yamdb", "api_yamdb.wsgi:application", "--bind", "0.0.0.0:8000"]
