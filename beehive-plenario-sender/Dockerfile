FROM waggle/beehive-server

ADD . /usr/lib/waggle/beehive-server/beehive-plenario-sender

RUN apt-get update && apt-get install -y \
    python3-pip 

# python modules
# Note regarding the mysql library (mysqlclient is a replacement for MySQL-python which has some python3 issues)

RUN pip3 install -r /usr/lib/waggle/beehive-server/beehive-plenario-sender/requirements.txt

WORKDIR /usr/lib/waggle/beehive-server/beehive-plenario-sender/

CMD ["python3", "plenario-sender.py"]

