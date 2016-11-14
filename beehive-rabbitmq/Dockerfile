FROM rabbitmq:3.5.6

COPY ./enabled_plugins /etc/rabbitmq/enabled_plugins
COPY ./rabbitmq.config /etc/rabbitmq/rabbitmq.config

RUN apt-get update && apt-get install -y python
COPY ./rabbitmqadmin /usr/bin/rabbitmqadmin
