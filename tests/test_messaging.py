from pytest import raises


def test_get_cmd_and_routing_key():
    from app.messaging import _get_cmd_and_routing_key

    event = {"type": "message", "text": "gcloud help"}
    key = _get_cmd_and_routing_key(event)
    assert key == "gcloud.#"

    event = {"type": "message", "text": "cv help"}
    key = _get_cmd_and_routing_key(event)
    assert key == "cv.#"

    with raises(KeyError):
        _get_cmd_and_routing_key({"type": "bot_message"})
