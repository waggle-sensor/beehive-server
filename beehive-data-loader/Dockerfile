FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY data-loader ./
CMD ["python", "data-loader", "--url", "amqp://router:router@beehive-rabbitmq", "0000000000000000"]
