import os
import sys
import hmac
import hashlib
from time import time
from functools import wraps

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class VerifySlackSignature(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        timestamp = request.headers.get("X-Slack-Request-Timestamp")
        if abs(time() - int(timestamp)) > 60 * 5:
            return Response("Invalid request timestamp", status_code=403)

        signature = request.headers.get("X-Slack-Signature")
        req = str.encode("v0:" + str(timestamp) + ":") + request.body()
        request_hash = (
            "v0="
            + hmac.new(str.encode(SIGNING_SECRET), req, hashlib.sha256).hexdigest()
        )
        # Compare byte strings for Python 2
        if sys.version_info[0] == 2:
            return hmac.compare_digest(bytes(request_hash), bytes(signature))
        else:
            return hmac.compare_digest(request_hash, signature)

        response = await call_next(request)
        response.headers["Custom"] = "Example"
        return response

