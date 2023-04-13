FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
COPY dev-requirements.txt dev-requirements.txt
RUN python3 -m venv venv 
RUN source venv/bin/activate
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r dev-requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=src.app:create_app
