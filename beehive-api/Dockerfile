
FROM waggle/beehive-server

RUN apt-get update && apt-get install -y python-mysqldb

RUN cd /usr/lib/waggle/beehive-server/beehive-api/ ; git pull

EXPOSE 80
WORKDIR /usr/lib/waggle/beehive-server/beehive-api/
CMD ["python", "-u", "/usr/lib/waggle/beehive-server/beehive-api/apiserver.py"]