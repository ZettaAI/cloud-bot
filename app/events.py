from pydantic import BaseModel


class AppMention(BaseModel):
    type: str
    user: str
    text: str
    ts: float
    channel: str
    event_ts: int


class Event(BaseModel):
    token: str
    team_id: str
    api_app_id: str
    event: AppMention
    type: str
    event_id: str
    event_time: int
    authed_users: list
