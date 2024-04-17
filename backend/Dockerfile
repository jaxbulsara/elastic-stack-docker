FROM    python:3.10-slim

RUN     pip install pipenv

WORKDIR /app
COPY    Pipfile* .
RUN     pipenv install --system

COPY    . .
