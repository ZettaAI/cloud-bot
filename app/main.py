from starlette.config import Config
from starlette.routing import Route
from starlette.requests import Request
from starlette.datastructures import Secret
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.applications import Starlette

from .middlewares import VerifySlackSignature

config = Config("deploy.env")
DEBUG = config("DEBUG", cast=bool, default=False)


async def homepage(request: Request):
    return JSONResponse({"hello": "world"})


async def mention(request: Request):
    print(request.state.json)
    return PlainTextResponse("helloooo!")


routes = [
    Route("/", homepage),
    Route("/events", endpoint=mention, methods=["POST"]),
]

middleware = [Middleware(VerifySlackSignature)]
app = Starlette(debug=DEBUG, routes=routes, middleware=middleware)
app.state.SLACK_API_TOKEN = config("SLACK_API_TOKEN", cast=Secret)
app.state.SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", cast=Secret)

