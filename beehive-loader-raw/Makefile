build:
	docker build -t waggle/beehive-loader-raw .

run:
	docker run --detach \
					   --net beehive \
						 --restart failure \
						 --name beehive-loader-raw \
						 beehive-loader-raw

start:
	systemctl start waggle/beehive-loader-raw

stop:
	systemctl stop waggle/beehive-loader-raw

restart:
	systemctl restart waggle/beehive-loader-raw
