FROM python:3

WORKDIR /usr/src/app

# install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy local scripts
COPY . .

ENV RABBITMQ_HOST=amqp://worker_gps-sense:worker@beehive-rabbitmq

CMD ["python", "./worker.py"]
