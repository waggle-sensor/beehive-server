FROM ubuntu:14.04

RUN apt-get update ; apt-get install -y git \
  python-dev python-pip \
  python3-dev python3-pip

ADD . /usr/lib/waggle/beehive-server/

# get submodule
RUN cd /usr/lib/waggle/beehive-server/ && \
  git submodule update --init

# python modules
RUN cd /usr/lib/waggle/beehive-server/ && \
  ./install_dependencies.sh 
  


ENV CASSANDRA_SERVER beehive-cassandra 

WORKDIR /usr/lib/waggle/beehive-server/
