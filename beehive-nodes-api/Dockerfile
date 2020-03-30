
FROM python:alpine

RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install mysqlclient Flask requests gunicorn;\
    apk del .build-deps 
# from https://github.com/gliderlabs/docker-alpine/issues/181
	
# OSX   
# export PATH=$PATH:/usr/local/Cellar/mysql-client/8.0.18/bin/


# Flask needs that
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=apiserver.py


# pip3 install cassandra-driver

# that is FLASK default port
EXPOSE 5000

COPY apiserver.py /code/
WORKDIR /code/

# development
#CMD ["flask", "run", "--host=0.0.0.0"]

#production
CMD ["gunicorn" , "-w 4", "-b 0.0.0.0:5000",  "apiserver:app"]
