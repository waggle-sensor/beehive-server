IMAGE = waggle/beehive-nginx
CONTAINER = beehive-nginx
SSL_PATH = /mnt/waggle/SSL/nginx/

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm -ti --name=$(CONTAINER) --net beehive -p 80:80 -p 443:443 -v $(SSL_PATH):/ssl $(IMAGE) /usr/sbin/nginx -g 'daemon off;'

start:
	docker run --rm --name=$(CONTAINER) --net beehive -p 80:80 -p 443:443 -v $(SSL_PATH):/ssl $(IMAGE) /usr/sbin/nginx -g 'daemon off;'
stop:
	docker rm -f beehive-nginx
clean:
	docker rm -f beehive-nginx
	docker rmi -f waggle/beehive-nginx

.PHONY: ssl

ssl:
	mkdir -p $(SSL_PATH)
	openssl genrsa -out $(SSL_PATH)/nginx.key 2048
	openssl req -new -key $(SSL_PATH)/nginx.key -out $(SSL_PATH)/nginx.csr
	openssl x509 -req -days 365 -in $(SSL_PATH)/nginx.csr -signkey $(SSL_PATH)/nginx.key -out $(SSL_PATH)/nginx.crt

