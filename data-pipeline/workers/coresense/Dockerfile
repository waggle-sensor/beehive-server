FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV RABBITMQ_HOST=amqp://worker_coresense:worker@beehive-rabbitmq

CMD ["python", "./worker.py"]
