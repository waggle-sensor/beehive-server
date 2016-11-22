build:
	docker build -t waggle/beehive-api .

start:
	systemctl start beehive-api

stop:
	systemctl stop beehive-api

restart:
	systemctl restart beehive-api

logs:
	journalctl -f -u beehive-api
