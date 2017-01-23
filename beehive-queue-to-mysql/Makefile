build:
	docker rm -f beehive-queue-to-mysql || echo 'no container to rm'
	docker rmi -f waggle/beehive-queue-to-mysql || echo 'no docker image to rm'
	docker build -t waggle/beehive-queue-to-mysql .

start:
	systemctl start beehive-queue-to-mysql

stop:
	systemctl stop beehive-queue-to-mysql

restart:
	systemctl restart beehive-queue-to-mysql

logs:
	journalctl -f -u beehive-queue-to-mysql

bash:
	echo 'bashing...'
	docker run --rm -ti --name beehive-queue-to-mysql --net beehive -v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/   -v /root/git/beehive-server/beehive-queue-to-mysql/:/usr/lib/waggle/beehive-server/beehive-queue-to-mysql waggle/beehive-queue-to-mysql:latest bash

run:
	echo 'running... ' 
	docker rm -f beehive-queue-to-mysql || echo "no container to rm"
	#docker run --rm -ti   --name beehive-db-decoded2   --net beehive  -v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/   waggle/beehive-server:latest bash -c 'git pull ; git submodule update --init ; ./configure && python3 -u ./QueueToDb.py decoded'

	#docker run --rm -ti --name beehive-queue-to-mysql --net beehive -v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/   -v /root/git/beehive-server/:/usr/lib/waggle/beehive-server/  -v /mnt/beehive:/mnt/beehive   waggle/beehive-queue-to-mysql:latest bash -c 'pwd;ls -l;git pull ; git submodule update --init ; ./configure && python3 -u ./QueueToMysql.py decoded -vvv'

	#docker run --rm -ti --name beehive-queue-to-mysql --net beehive -v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/   -v /root/git/beehive-server/:/usr/lib/waggle/beehive-server/  -v /mnt/beehive:/mnt/beehive   waggle/beehive-queue-to-mysql:latest bash -c 'pwd;ls -l;python3 -u ./QueueToMysql.py decoded -vvv'

	docker run --rm -ti --name beehive-queue-to-mysql --net beehive -v /mnt/waggle/SSL/:/usr/lib/waggle/SSL/   -v /root/git/beehive-server/:/usr/lib/waggle/beehive-server/  -v /mnt/beehive:/mnt/beehive   waggle/beehive-server:latest bash -c 'pwd; ls ; git pull ; git submodule update --init ; ./configure && python3 -u  ./beehive-queue-to-mysql/QueueToMysql.py decoded -vvv'

