from enum import Enum


class EventTypes(Enum):
    MESSAGE = "message"
    APP_MENTION = "app_mention"
    BOT_MESSAGE = "bot_message"
