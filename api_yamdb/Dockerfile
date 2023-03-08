FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY api_yamdb/requirements.txt /app/
RUN pip install -r requirements.txt

COPY api_yamdb /app/

EXPOSE 8000

CMD ["gunicorn", "--chdir", "api_yamdb", "--bind", ":8000", "wsgi:application"]
