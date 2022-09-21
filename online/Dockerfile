# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
<<<<<<< HEAD
WORKDIR /app/app
CMD ["python", "-u", "main.py"]
=======

CMD [ "python3", "main.py"]
>>>>>>> 3f70f064e773b396540d0bc747ab3bc70203319c
