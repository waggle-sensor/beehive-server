FROM ubuntu:14.04

RUN apt-get update ; apt-get install -y git \
  python-dev python-pip

ADD . /usr/lib/waggle/beehive-server/

# python modules
RUN cd /usr/lib/waggle/beehive-server/packages_o/ && \
  pip install blist && \
  pip install cassandra-driver && \
  pip install crcmod && \
  cd pika-0.9.14/ && \
  python setup.py install

# cqlshlib for the cassandra client
RUN cd /usr/lib/waggle/beehive-server/cassandra-pylib/ && \
  python ./setup.py install  

ENV CASSANDRA_SERVER cassandra 

WORKDIR /usr/lib/waggle/beehive-server/
