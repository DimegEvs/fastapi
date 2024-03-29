FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x /app/docker/app.sh
