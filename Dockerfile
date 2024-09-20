# syntax=docker/dockerfile:1

FROM python:3.10-slim AS builder

LABEL maintainer="Richard Mwewa <https://gravatar.com/rly0nheart>"
LABEL description="A Reddit data analysis toolkit."

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install poetry && poetry install

FROM gcr.io/distroless/python3

COPY --from=builder /app /app

WORKDIR /app

ENTRYPOINT ["knewkarma"]
