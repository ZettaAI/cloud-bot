from starlette.requests import Request
from starlette.responses import Response

from .messaging import publish


async def homepage(request: Request):
    return Response("zzz...")


async def mention(request: Request):
    # print(request.state.json)
    publish(request)
    return Response(request.state.json.get("challenge"))
