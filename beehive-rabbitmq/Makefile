IMAGE = waggle/beehive-rabbitmq
CONTAINER = beehive-rabbitmq

build:
	docker build -t $(IMAGE) .

run:
	bin/docker run \
	--rm \
	--net beehive \
	--hostname $(CONTAINER) \
	--name ${CONTAINER} \
	-e RABBITMQ_NODENAME=${CONTAINER} \
	-v /mnt/rabbitmq/config/:/etc/rabbitmq:rw \
	-v /mnt/rabbitmq/data/:/var/lib/rabbitmq/:rw \
	-v /mnt/waggle/SSL:/usr/lib/waggle/SSL/:ro \
	-p 127.0.0.1:5672:5672 \
	-p 23181:23181 \
	-p 15672:15672 \
	$(IMAGE)
