# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

FROM ubuntu:18.04

EXPOSE 80
RUN apt-get update && apt-get install -y openssh-client openssl python3-mysqldb python3-webpy python3-requests

WORKDIR /usr/lib/waggle/beehive-server/beehive-cert/
COPY . .

CMD ["python3", "./cert-serve.py"]
