
FROM waggle/beehive-server

RUN apt-get update && apt-get install -y python-mysqldb


EXPOSE 80
WORKDIR /usr/lib/waggle/beehive-server/beehive-web/
CMD ["python", "-u", "/usr/lib/waggle/beehive-server/beehive-web/webserver.py"]