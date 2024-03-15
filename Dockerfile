FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

ENV FLASK_APP app.py

ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "3000"]
