# comment

FROM rabbitmq:3.5.6

RUN apt-get update -y && \
	apt-get install -y \
		curl \
		git \
		python-dev python-pip

RUN curl https://raw.githubusercontent.com/rabbitmq/rabbitmq-management/rabbitmq_v3_6_5/bin/rabbitmqadmin -o /usr/bin/rabbitmqadmin

RUN chmod +x /usr/bin/rabbitmqadmin

# RUN python /usr/bin/rabbitmqadmin list exchanges

