FROM ubuntu:16.04

EXPOSE 80
RUN apt-get update && apt-get install -y openssh-client openssl python-mysqldb python-webpy

WORKDIR /usr/lib/waggle/beehive-server/beehive-cert/
COPY . .

CMD ["python", "./cert-serve.py"]
