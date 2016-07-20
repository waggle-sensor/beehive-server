FROM nginx:1.10.1

# or nginx:1.10.1-alpine

ADD beehive.conf /etc/nginx/conf.d/beehive.conf

RUN rm /etc/nginx/conf.d/default.conf

# this CMD does not work
#CMD ["/usr/sbin/nginx", "-g 'daemon off;'"]