import os
import sys
import hmac
import json
import hashlib
from time import time
from functools import wraps
from typing import Tuple

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


def _verify(request: Request) -> Tuple[bool, Response]:
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    if abs(time() - int(timestamp)) > 60 * 5:
        return False, Response("Invalid request timestamp.", status_code=403)

    req_bytes = await request.body()
    request.state.json = json.loads(req_bytes)

    signature = request.headers.get("X-Slack-Signature")
    req = str.encode("v0:" + str(timestamp) + ":") + req_bytes
    SECRET = str(request.app.state.SLACK_SIGNING_SECRET)
    rhash = "v0=" + hmac.new(str.encode(SECRET), req, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(rhash, signature):
        return False, Response("Invalid request.", status_code=403)
    return True, None


class VerifySlackSignature(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "/events" in request.url.path:
            success, response = _verify(request)
            if not success:
                return response
        return await call_next(request)

