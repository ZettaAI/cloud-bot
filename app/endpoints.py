from json import loads

from starlette.requests import Request
from starlette.responses import Response

from .messaging import publish


###########################
# Initial slack verfication
###########################


async def verify(request: Request):
    req_bytes = await request.body()
    return Response(loads(req_bytes)["challenge"])


##########
# Main App
##########


async def homepage(request: Request):
    return Response("zzz...")


async def mention(request: Request):
    # print(request.state.json)
    publish(request)
    return Response(request.state.json.get("challenge"))
