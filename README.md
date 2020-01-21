# Cloud Bot

Slack bot to automate stuff on cloud.

The server receives messages from Slack's Events API.
A message exchange (RabbitMQ) is used to send these messages to workers.

## For development
Start the server with `uvicorn --reload app.main:app --host 0.0.0.0 --port 80`

The follwing environment variables are required:
```
DEBUG=
SLACK_SIGNING_SECRET=
AMQP_SERVICE_HOST=
GCLOUD_PROJECT=
GOOGLE_APPLICATION_CREDENTIALS=
```