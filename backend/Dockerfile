FROM    python:3.12.3-slim

RUN     pip install pipenv

WORKDIR /app
COPY    Pipfile* .
RUN     pipenv install --system

COPY    . .
