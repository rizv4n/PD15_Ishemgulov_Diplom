FROM python:3.10-slim

WORKDIR /todolist
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /todolist/manage.py .
COPY migartions migrations
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80