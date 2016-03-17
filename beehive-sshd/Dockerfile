
FROM waggle/beehive-server:latest


# delete files due to Hash Sum mismatch in Ubuntu 16.04: rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
  apt-get install -y openssh-server python git python-mysqldb


RUN mkdir -p /var/run/sshd /root/.ssh/ 

#RUN echo 'root:test' | chpasswd

RUN sed -i -e 's/^.\?PermitRootLogin.*/PermitRootLogin yes/' \
    -e 's/^.\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
    -e 's/^.\?PasswordAuthentication.*/PasswordAuthentication no/' \
    -e 's/^.\?UsePAM.*/UsePAM no/' \
    -e 's/^.\?LogLevel.*/LogLevel DEBUG/' \
    -e 's:^.\?AuthorizedKeysFile.*:AuthorizedKeysFile /usr/lib/waggle/SSL/nodes/authorized_keys:' \
    /etc/ssh/sshd_config


#TODO create dedicated user ! (either login as user or run sshd as user)

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
#CMD ["/usr/sbin/sshd", "-D"]
WORKDIR /usr/lib/waggle/beehive-server/beehive-sshd/
