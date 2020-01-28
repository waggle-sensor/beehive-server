
# beehive-nginx


Due to the static behaviour of nginx, nginx will fail to start if a backend server is missing. Thus, by default, all nginx locations are in include files, which can be activated by symlinks. The `update_nginx_config` script will determine the state of backend servers and create or delete symlinks in the nginx inlude directories to make sure the nginx config reflects the state of backend services.



