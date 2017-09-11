dodeploy() {
  cd $1
  make deploy
  cd ..
}

dodeploy beehive-cert
dodeploy beehive-flask
dodeploy beehive-loader-decoded
dodeploy beehive-loader-raw
dodeploy beehive-log-saver
dodeploy beehive-mysql
dodeploy beehive-nginx
dodeploy beehive-rabbitmq
dodeploy beehive-sshd
dodeploy beehive-worker-alphasense
dodeploy beehive-worker-coresense
dodeploy beehive-worker-gps
