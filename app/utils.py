import hmac
from json import dumps
from hashlib import sha256
from starlette.requests import Request


def verify_request(request: Request, req_bytes: bytes) -> bool:
    """
    See https://api.slack.com/docs/verifying-requests-from-slack
    
    The request body is stored in request state because await can only be called once.
    JSON loads and dumps are not guaranteed to produce same strings
    so passing `req_bytes` is necessary.
    """
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    req = str.encode(f"v0:{str(timestamp)}:") + req_bytes
    SECRET = str(request.app.state.SLACK_SIGNING_SECRET)
    rhash = "v0=" + hmac.new(str.encode(SECRET), req, sha256).hexdigest()
    return hmac.compare_digest(rhash, signature)
