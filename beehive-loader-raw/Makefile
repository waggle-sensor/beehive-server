name = beehive-loader-raw
image = waggle/$(name)

build:
	docker build -t $(image) .

run:
	docker run --detach --net beehive --restart=on-failure:10 --name $(name) $(image)

start:
	docker start $(name)

stop:
	docker stop $(name)

restart:
	docker restart $(name)
