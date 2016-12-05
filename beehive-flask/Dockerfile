
FROM waggle/beehive-server

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libmysqlclient-dev

# python modules
# Note regarding the mysql library (mysqlclient is a replacement for MySQL-python which has some python3 issues)

RUN pip3 install \
    mysqlclient \
    Flask \
    cassandra-driver \
    git+https://github.com/waggle-sensor/pywaggle


# Flask needs that
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=run.py


# pip3 install cassandra-driver

# that is FLASK default port
EXPOSE 5000

WORKDIR /usr/lib/waggle/beehive-server/beehive-flask/

#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python3", "run.py", "--host=0.0.0.0"]
#CMD ["pwd"]

