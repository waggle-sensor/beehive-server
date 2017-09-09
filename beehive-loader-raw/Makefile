build:
	docker build -t waggle/beehive-loader-raw .

run:
	docker run --detach --net beehive --restart=on-failure:10 --name beehive-loader-raw waggle/beehive-loader-raw

start:
	docker start waggle/beehive-loader-raw

stop:
	docker stop waggle/beehive-loader-raw

restart:
	docker restart waggle/beehive-loader-raw
