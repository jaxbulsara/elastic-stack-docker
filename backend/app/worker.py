import hashlib
import logging

from celery import Celery

from .log import handler

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(handler)

BROKER_URL = "amqp://celery-rabbitmq"
BACKEND_URL = "rpc://celery-redis"
celery = Celery("app", broker=BROKER_URL, backend=BACKEND_URL)

log.debug("Set up worker.")


@celery.task()
def calculate_hash(message: str):
    log.info("Starting 'calculate_hash' task: '%s'", message)
    return hashlib.sha256(message.encode()).hexdigest()
