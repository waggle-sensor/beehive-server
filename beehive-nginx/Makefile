IMAGE = waggle/beehive-nginx
CONTAINER = beehive-nginx

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm --name=$(CONTAINER) --net beehive -p 80:80 -p 443:443 -v /mnt/waggle/SSL/nginx/:/ssl $(IMAGE) /usr/sbin/nginx -g 'daemon off;'

.PHONY: ssl

ssl:
	mkdir -p ssl
	openssl genrsa -out ssl/nginx.key 2048
	openssl req -new -key ssl/nginx.key -out ssl/nginx.csr
	openssl x509 -req -days 365 -in ssl/nginx.csr -signkey ssl/nginx.key -out ssl/nginx.crt
