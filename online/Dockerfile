# syntax=docker/dockerfile:1

# FROM python:3.8

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .

# CMD [ "python3", "main.py"]

FROM neo4j AS builder

WORKDIR /app



FROM python:3.8 as python

RUN pip install --upgrade pip
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app/app
RUN file="$(ls)" && echo $file
RUN file="$(pwd)" && echo $file

CMD ["python3", "main.py"]