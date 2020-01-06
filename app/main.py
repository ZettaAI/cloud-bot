from json import dumps

import pika

from . import config
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.applications import Starlette

from . import endpoints
from .events import publish
from .messaging import get_ampq_connection
from .middlewares import VerifySlackSignature


routes = [
    Route("/", endpoints.homepage),
    Route("/events", endpoint=endpoints.mention, methods=["POST"]),
]

middleware = [Middleware(VerifySlackSignature)]
app = Starlette(debug=config.DEBUG, routes=routes, middleware=middleware)
app.state.exchange_cnxn = get_ampq_connection()
app.state.SLACK_SIGNING_SECRET = config.SLACK_SIGNING_SECRET

