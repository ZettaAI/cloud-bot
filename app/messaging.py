from typing import Dict

from starlette.requests import Request
from pika import BlockingConnection
from pika.channel import Channel


def get_ampq_connection() -> BlockingConnection:
    from pika import ConnectionParameters
    from .config import AMQP_CREDS
    from .config import AMQP_SERVICE_HOST

    return BlockingConnection(
        ConnectionParameters(
            host=AMQP_SERVICE_HOST, credentials=AMQP_CREDS, heartbeat=0
        )
    )


def _get_channel(request: Request) -> Channel:
    try:
        channel = request.app.state.amqp_channel
        channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")
    except:
        request.app.state.amqp_cnxn = get_ampq_connection()
        channel = request.app.state.amqp_cnxn.channel()
        request.app.state.amqp_channel = channel
        channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")
    return channel


def _get_cmd_and_routing_key(event: Dict) -> str:
    """
    Parse user text to extract command and get routing key for appropriate worker.
    Updates the event json to include extracted command (`user_cmd`).
    """
    from .slack import EventTypes
    from .utils import parse_slack_message

    cmd_txt = event["text"]
    cmd_txt = (
        cmd_txt.split(" ", 1)[-1]
        if event["type"] == EventTypes.APP_MENTION.value
        else cmd_txt
    )
    event["user_cmd"] = parse_slack_message(cmd_txt)
    return f"{event['user_cmd'].split()[0]}.#"


def publish(request: Request) -> None:
    from json import dumps

    try:
        event = request.state.json["event"]
        r_key = _get_cmd_and_routing_key(event)
    except KeyError:
        # this event is not relevant so ignore
        return

    channel = _get_channel(request)
    channel.basic_publish(
        exchange="cloud_bot", routing_key=r_key, body=dumps(request.state.json)
    )
