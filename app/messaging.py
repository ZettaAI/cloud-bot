from json import dumps

import pika

from .slack import EventTypes
from .config import AMQP_CREDS
from .config import AMQP_SERVICE_HOST
from .utils import parse_slack_message


def get_ampq_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=AMQP_SERVICE_HOST, credentials=AMQP_CREDS, heartbeat=0
        )
    )


def publish(request):
    try:
        channel = request.app.state.amqp_channel
        channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")
    except:
        request.app.state.amqp_cnxn = get_ampq_connection()
        channel = request.app.state.amqp_cnxn.channel()
        request.app.state.amqp_channel = channel
        channel.exchange_declare(exchange="cloud_bot", exchange_type="topic")

    try:
        event = request.state.json["event"]
        cmd_txt = event["text"]
    except KeyError:
        # this event is not relevant so return
        return
    cmd_txt = (
        cmd_txt.split(" ", 1)[-1]
        if event["type"] == EventTypes.APP_MENTION.value
        else cmd_txt
    )
    cmd_txt = parse_slack_message(cmd_txt)
    r_key = f"{cmd_txt.split()[0]}.#"

    event["user_cmd"] = cmd_txt
    channel.basic_publish(
        exchange="cloud_bot", routing_key=r_key, body=dumps(request.state.json)
    )
