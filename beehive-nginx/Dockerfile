FROM nginx:1.10.1-alpine

# or nginx:1.10.1

ADD beehive.conf /etc/nginx/conf.d/beehive.conf

RUN rm /etc/nginx/conf.d/default/conf


CMD ["/usr/sbin/nginx", "-g 'daemon off;'"]