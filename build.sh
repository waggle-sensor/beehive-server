dobuild() {
  cd $1
  make build
  cd ..
}

dobuild beehive-cert
dobuild beehive-flask
dobuild beehive-loader-decoded
dobuild beehive-loader-raw
dobuild beehive-log-saver
dobuild beehive-nginx
dobuild beehive-rabbitmq
dobuild beehive-sshd
dobuild beehive-worker-alphasense
dobuild beehive-worker-coresense
dobuild beehive-worker-gps
