FROM    python:3.10-slim

VOLUME  /var/logs

WORKDIR /app

COPY    requirements.txt .

RUN     pip install --no-cache-dir -r requirements.txt

COPY    . .

RUN     mkdir /logs

CMD     ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
