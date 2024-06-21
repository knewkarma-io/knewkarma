# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install poetry && poetry install

ENTRYPOINT ["poetry", "run", "knewkarma"]
