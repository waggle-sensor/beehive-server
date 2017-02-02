FROM python:3-onbuild
ENV RABBITMQ_HOST=amqp://worker_alphasense:worker@beehive-rabbitmq
CMD ["python", "./worker.py"]
