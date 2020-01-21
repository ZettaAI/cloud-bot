from json import dumps
from google.cloud import firestore

from .slack import EventTypes

db = firestore.Client()


def add_event(event: dict) -> None:
    try:
        doc_ref = db.collection("events").document(event["event_ts"])
        doc_ref.set({"body": dumps(event)})
    except Exception as err:
        print(err)
