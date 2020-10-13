def test_get_datasets():
    from app.utils import parse_slack_message

    msg = "this is a test, user name: <I9DXIK54>, email: <test@email.com>"
    msg = parse_slack_message(msg)
    for c in ["<", ">"]:
        assert c not in msg
