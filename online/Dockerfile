FROM neo4j AS builder

WORKDIR /app

FROM python:3.8 as python

# RUN pip install upgrade pip
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app/app

CMD ["python3", "main.py"]