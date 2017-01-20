
FROM waggle/beehive-server

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libmysqlclient-dev

# python modules
# Note regarding the mysql library (mysqlclient is a replacement for MySQL-python which has some python3 issues)

RUN pip3 install \
    mysqlclient \
    git+https://github.com/waggle-sensor/pywaggle

WORKDIR /usr/lib/waggle/beehive-server/

#CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["python3", "run.py", "--host=0.0.0.0"]
