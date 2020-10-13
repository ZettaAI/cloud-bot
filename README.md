[![Build Status](https://api.travis-ci.org/ZettaAI/cloud-bot.svg?branch=master)](https://travis-ci.org/ZettaAI/cloud-bot)



## Cloud Bot

Slack bot to automate stuff on cloud.

The server receives messages from Slack's Events API.
A message exchange (RabbitMQ) is used to send these messages to workers.

### For development
Start the server with `uvicorn --reload app.main:app --host 0.0.0.0 --port 80`
