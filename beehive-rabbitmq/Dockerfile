# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license

FROM rabbitmq:3.5.7

ADD configs/enabled_plugins /etc/rabbitmq/enabled_plugins
ADD configs/rabbitmq.config /etc/rabbitmq/rabbitmq.config
ADD configs/definitions.json /etc/rabbitmq/definitions.json

EXPOSE 5671/tcp
EXPOSE 15672/tcp
