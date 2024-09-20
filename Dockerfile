# syntax=docker/dockerfile:1

FROM python:3.10-slim

LABEL maintainer="Richard Mwewa <https://gravatar.com/rly0nheart>"
LABEL description="A Reddit data analysis toolkit."

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install poetry && poetry install

ENTRYPOINT ["poetry", "run", "knewkarma"]
