# get the base image
FROM python:3.8

# specify working directory inside the container
WORKDIR /code

# copy requirements into the container
COPY requirements.txt requirements.txt
 
# install the requirements inside the container
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy project files into the container
COPY . .

# run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
