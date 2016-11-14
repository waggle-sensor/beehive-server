build:
	docker build -t beehive-nginx-tls .

run:
	docker run --rm --name=beehive-nginx --net beehive -p 80:80 -p 443:443 -v /mnt/waggle/SSL/nginx/:/ssl beehive-nginx-tls /usr/sbin/nginx -g 'daemon off;'
