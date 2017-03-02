#!/bin/bash
# Must be run after superuser -i command:
### sudo -i
set -v -x 

if true; then
    if true; then
        #####################################################################
        #########   UN-INSTALL old beehive server
        #####################################################################
        echo "WARNING:  You are about to UNINSTALL the beehive!!!!"
        echo -n  "Are you sure? ('Yes' to continue) > "
        read confirmation
        echo confirmation = "$confirmation"
        if [ "$confirmation" == "Yes" ]; then
            set -v -x
            echo "UN-INSTALLing beehive..."
            ## files in $DATE=/mnt
            rm -rf /mnt/cassandra  /mnt/mysql  /mnt/rabbitmq  /mnt/ssh_keys  /mnt/waggle

            ##-- systemd
            cd /etc/systemd/system
            for s in $(systemctl list-units --plain '*beehive*' | grep beehive | awk '{print $1}'); do
                systemctl stop $s
                systemctl disable $s
                systemctl reset-failed $s
            done
            rm -f /etc/systemd/system/*beehive-*.service

            systemctl status beehive-*  --no-pager -l
            systemctl list-units 'beehive-*' --all
            systemctl daemon-reload

            ##-- docker containers
            echo "BEFORE removal...."
            docker ps -a
            for container in `docker ps -aq`; do
                echo ' removing container ' $container
                docker rm -fv $container
            done
            for image in `docker images -aq`; do
                echo ' removing container image ' $image
                docker rmi -f $image
            done
            
            bash /root/git/beehive-server/scripts/docker_cleanup.sh
            
            echo "AFTER removal...."
            docker ps -a
            docker images -a
            docker volume ls
            service docker stop
            rm -rf /var/lib/docker/aufs

            echo "UNInstall COMPLETE."
        else
            echo "Uninstall ABORTed."
        fi
    fi
    #####################################################################
    #########   INSTALL
    #####################################################################
    
    #### First, do all the pieces that require user-input 
    
    # beehive-config.json
    mkdir -p /mnt/beehive
    echo; echo; echo "*** YOU MUST edit /mnt/beehive/beehive-config.json specific to this beehive server"
    echo " If you have not customized this file yet, go do it now."
    echo " If you have customized this file, and want to continue, enter 'Yes'."
    read confirmation
    echo confirmation = "$confirmation"
    if [ "$confirmation" != "Yes" ]; then
        exit
    fi
    
    cp -i beehive-config.json /mnt/beehive
    
    # NGINX needs SSL keys
    echo; echo; echo "NGINX SSL keys need the following information..."
    cd ~/git/beehive-server/beehive-nginx
    make ssl
    echo "NGINX SSL keys created"
    echo; echo

    # The rest is autonomous - does not require user input - and takes a while
    apt-get install -y curl
    apt-get install -y git
    apt update
    
    cd ~
    rm -rf git
    mkdir -p git
    cd git
    git clone https://github.com/waggle-sensor/beehive-server.git
    cd ~/git/beehive-server/
    
    #### Docker
    apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    export CODENAME=$(lsb_release --codename | grep -o "[a-z]*$" | tr -d '\n')
    echo "deb https://apt.dockerproject.org/repo ubuntu-${CODENAME} main" > /etc/apt/sources.list.d/docker.list
    apt-get update
    apt-get install -y  docker-engine
    service docker restart
    docker --version
    
    export DATA="/mnt"
    echo "export DATA=/mnt/" >> ~/.bash_profile
    docker network create beehive

    docker network ls
    docker network inspect beehive

    #apt-get install -y python-webpy

    # pull all the images we have in the docker hub
    docker pull cassandra:3.2
    docker pull mysql:5.7.10
    docker pull rabbitmq:3.5.6
    docker pull waggle/beehive-cert:latest
    docker pull waggle/beehive-sshd:latest
    docker pull waggle/beehive-server:latest
    
    # build all the images that need to be built
    for a in \
        /root/git/beehive-server/beehive-flask/                     \
        /root/git/beehive-server/beehive-nginx/                     \
        /root/git/beehive-server/beehive-plenario-sender/           \
        /root/git/beehive-server/beehive-queue-to-mysql/            \
        /root/git/beehive-server/beehive-rabbitmq/                  \
        /root/git/beehive-server/data-pipeline/workers/gps-sense/   \
        /root/git/beehive-server/data-pipeline/workers/alphasense/  \
        /root/git/beehive-server/data-pipeline/workers/coresense/
    do
        echo
        echo $a
        cd $a
        make build
    done
    
    ### SSL
    [ ! -z "$DATA" ] && docker run -ti \
      --name certs \
      --rm \
      -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
      waggle/beehive-server:latest ./SSL/create_certificate_authority.sh

    ### RabbitMQ - this must run BEFORE RabbitMQ container is up
    mkdir -p ${DATA}/rabbitmq/config/ && \
    curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-rabbitmq/rabbitmq.config > ${DATA}/rabbitmq/config/rabbitmq.config

    [ ! -z "$DATA" ] && docker run -ti \
      --name certs \
      --rm \
      -v ${DATA}/waggle/SSL/:/usr/lib/waggle/SSL/ \
      waggle/beehive-server:latest ./SSL/create_server_cert.sh

    chmod +x ${DATA}/waggle/SSL/server

    ### systemd  - start all the services once the containers are available
    cd ~/git/beehive-server/systemd/
      
    for service in *.service ; do
        echo "Deploy ${service}"
        rm -f /etc/systemd/system/${service}
        cp ${service} /etc/systemd/system
        systemctl daemon-reload
        systemctl enable ${service}
        systemctl start ${service}
        #systemctl status ${service}  --no-page -l
    done
    
    sleep 10
    
    systemctl status '*beehive*'  --no-page -l
    
    date

    # after beehive-mysql is running
    while true; do
        curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-mysql/createTablesMysql.sql | docker exec -i beehive-mysql mysql -u waggle --password=waggle \
        && break
      sleep 10
      nTries=$[$nTries+1]
      echo "  mysql try #" $nTries " ..."
    done
      
    
    # after beehive-cassandra is running
    sleep 20
    while true; do
        curl https://raw.githubusercontent.com/waggle-sensor/beehive-server/master/beehive-cassandra/createTablesCassandra.sql | docker exec -i beehive-cassandra cqlsh \
        && break
      sleep 10
      nTries=$[$nTries+1]
      echo "  mysql try #" $nTries " ..."
    done


    # after beehive-rabbitmq is up
    nTries=0
    sleep 20
    while true
    do docker exec -ti  beehive-rabbitmq bash -c '\
            rabbitmqctl add_user node waggle  ; \
            rabbitmqctl add_user server waggle  ; \
            rabbitmqctl set_permissions node "node_.*" ".*" ".*"  ; \
            rabbitmqctl set_permissions server ".*" ".*" ".*"  ; \
            rabbitmq-plugins enable rabbitmq_auth_mechanism_ssl' \
            && break
      sleep 10
      nTries=$[$nTries+1]
      echo "rabbitmqctl try #" $nTries " ..."
    done
fi 
echo 'DONE'
date