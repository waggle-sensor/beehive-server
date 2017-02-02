FROM python:3-onbuild
ENV RABBITMQ_HOST=amqp://worker_gps-sense:worker@beehive-rabbitmq
CMD ["python", "./worker.py"]
