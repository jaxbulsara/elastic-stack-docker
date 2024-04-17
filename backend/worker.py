from celery import Celery


broker_url = 'amqp://celery-rabbitmq'
backend_url = 'rpc://celery-redis'
celery = Celery('app', broker=broker_url, backend=backend_url)

@celery.task()
def calculate_hash(message: str):
    return hashlib.sha256(message.encode()).hexdigest()
