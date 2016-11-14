IMAGE = waggle/beehive-nginx
CONTAINER = beehive-nginx

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm --name=$(CONTAINER) --net beehive -p 80:80 -p 443:443 -v /mnt/waggle/SSL/nginx/:/ssl $(IMAGE) /usr/sbin/nginx -g 'daemon off;'
