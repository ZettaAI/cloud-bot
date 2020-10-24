[![Build Status](https://api.travis-ci.org/ZettaAI/cloud-bot.svg?branch=master)](https://travis-ci.org/ZettaAI/cloud-bot)



## Cloud Bot

Slack bot to automate stuff on cloud.

The bot server receives messages from Slack's Events API.
A message exchange (RabbitMQ) is used to send these messages to workers.


### Example worker depoyment

You can find details of deployment in the `example/deploy` folder. This assumes that you have already setup the bot in your Slack's app management page.

#### RabbitMQ

The easiest way to install/deploy is with `helm` charts. First install rabbitmq:

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm install my-release bitnami/rabbitmq
$ cd example/deploy
$ helm install rabbit bitnami/rabbitmq -f rabbitmq.yml
```

This will create a RabbitMQ service and its deployment. More details about the chart [here](https://github.com/bitnami/charts/tree/master/bitnami/rabbitmq).

In addition, the environment variables `AMQP_SERVICE_HOST` and `AMQP_SERVICE_PORT` are added to bot server and worker pods.


#### Bot Server and Workers

Refer to `values.yml` for required variables, mainly values required by Slack.

Add Zetta's `helm` repo and update dependencies to install required sub-charts.

```
$ helm repo add zetta http://zetta.ai/helm-charts/charts
$ helm repo update
$ helm dependencies update
$ helm install --debug <release-name> .
```

#### Installing workers independently

It is easy to install or deploy just a single worker or a group of related workers as a `helm` release.
Make sure to add the required environment variables so that workers can connect to the message exchange.


#### Supported message types

A worker can respond to DMs, channels and threads. Refer to different command types in `example/example-workers`. Responding to threads is especcially helpful for long tasks and providing updates at checkpoints in a thread, use `broadcast=True` to notify channel for important checkpoints.

Python package `click` is used to parse user commands, it provides great support for various use cases.
