from json import loads
from time import time

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from .utils import verify_request


class VerifySlackSignature(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "/events" in request.url.path:
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            if abs(time() - int(timestamp)) > 60 * 5:
                return False, Response("Invalid request timestamp.", status_code=403)

            request.state.json = loads(await request.body())
            if not verify_request(request):
                return False, Response("Invalid request.", status_code=403)
        return await call_next(request)

