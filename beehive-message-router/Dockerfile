FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY beehive-message-router ./
CMD ["python", "./beehive-message-router", "--url", "amqp://rabbitmq", "messages"]
