import hmac
from json import dumps
from hashlib import sha256
from starlette.requests import Request


def verify_request(request: Request, req_bytes: bytes) -> bool:
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    req = str.encode(f"v0:{str(timestamp)}:") + req_bytes
    SECRET = str(request.app.state.SLACK_SIGNING_SECRET)
    rhash = "v0=" + hmac.new(str.encode(SECRET), req, sha256).hexdigest()
    return hmac.compare_digest(rhash, signature)
