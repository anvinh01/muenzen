FROM python:3.10.6-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]

