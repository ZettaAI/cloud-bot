import pika
from starlette.config import Config
from starlette.datastructures import Secret

config = Config("deploy.env")

DEBUG = config("DEBUG", cast=bool, default=True)
AMQP_CREDS = pika.credentials.PlainCredentials(
    config.get("AMQP_USERNAME", default="guest"),
    config.get("AMQP_PASSWORD", default="guest"),
)
AMQP_SERVICE_HOST = config.get("AMQP_SERVICE_HOST", default="localhost")
SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", cast=Secret)
