build:
	docker build -t waggle/beehive-flask .

start:
	systemctl start beehive-flask

stop:
	systemctl stop beehive-flask

restart:
	systemctl restart beehive-flask

logs:
	journalctl -f -u beehive-flask
