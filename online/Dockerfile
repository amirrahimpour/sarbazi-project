# syntax=docker/dockerfile:1

# pull base image
FROM python:3.8

# specify the working directory inside container
WORKDIR /app

# copy requirements file into the container
COPY requirements.txt requirements.txt

# install the requirements
RUN pip3 install -r requirements.txt

# copy project files into the container
COPY . .

# cd to the folder containing main.py inside the container
WORKDIR /app/app

# run the application
CMD ["python", "-u", "main.py"]
