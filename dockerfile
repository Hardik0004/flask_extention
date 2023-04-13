FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
COPY dev-requirements.txt dev-requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=src.app:create_app
