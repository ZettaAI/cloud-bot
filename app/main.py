from json import dumps

import pika
from starlette.config import Config
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.datastructures import Secret

from .middlewares import VerifySlackSignature

config = Config("deploy.env")
DEBUG = config("DEBUG", cast=bool, default=False)
AMQP_CREDS = pika.credentials.PlainCredentials(
    config.get("AMQP_USERNAME", default="guest"),
    config.get("AMQP_PASSWORD", default="guest"),
)
AMQP_SERVICE_HOST = config.get("AMQP_SERVICE_HOST", default="localhost")


def publish(connection, message):
    channel = connection.channel()
    channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")
    channel.basic_publish(exchange="cloud_bot", routing_key="gcloud.#", body=message)


async def homepage(request: Request):
    return Response()


async def mention(request: Request):
    print(request.state.json)
    publish(request.app.state.exchange_cnxn, dumps(request.state.json))
    return Response()


routes = [
    Route("/", homepage),
    Route("/events", endpoint=mention, methods=["POST"]),
]

middleware = [Middleware(VerifySlackSignature)]
app = Starlette(debug=DEBUG, routes=routes, middleware=middleware)
app.state.exchange_cnxn = pika.BlockingConnection(
    pika.ConnectionParameters(host=AMQP_SERVICE_HOST, credentials=AMQP_CREDS)
)
app.state.SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", cast=Secret)

