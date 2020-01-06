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

from .slack import EventTypes
from .middlewares import VerifySlackSignature

config = Config("deploy.env")
DEBUG = config("DEBUG", cast=bool, default=False)
AMQP_CREDS = pika.credentials.PlainCredentials(
    config.get("AMQP_USERNAME", default="guest"),
    config.get("AMQP_PASSWORD", default="guest"),
)
AMQP_SERVICE_HOST = config.get("AMQP_SERVICE_HOST", default="localhost")


def publish(request):
    try:
        channel = request.app.state.exchange_cnxn.channel()
    except:
        request.app.state.exchange_cnxn = pika.BlockingConnection(
            pika.ConnectionParameters(host=AMQP_SERVICE_HOST, credentials=AMQP_CREDS)
        )
        channel = request.app.state.exchange_cnxn.channel()

    event = request.state.json["event"]
    cmd_txt = event["text"]
    cmd_txt = (
        cmd_txt.split(" ", 1) if event["type"] == EventTypes.APP_MENTION else cmd_txt
    )
    r_key = f"{cmd_txt.split()[0]}.#"
    channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")

    event["user_cmd"] = cmd_txt
    channel.basic_publish(
        exchange="cloud_bot", routing_key=r_key, body=dumps(request.state.json)
    )


async def homepage(request: Request):
    return Response()


async def mention(request: Request):
    print(request.state.json)
    publish(request)
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

