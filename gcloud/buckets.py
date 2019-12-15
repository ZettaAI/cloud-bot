import os

import slack
from google.cloud import storage

client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])


storage_client = storage.Client()
bucket_name = "akhilesh-test2"
bucket = storage_client.create_bucket(bucket_name)

response = client.chat_postMessage(channel="#general", text=f"{bucket.name} created!")
assert response["ok"]

