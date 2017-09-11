FROM ubuntu:16.04

RUN apt-get update && apt-get install -y openssh-server curl netcat net-tools
RUN mkdir -p /var/run/sshd

RUN echo 'root:waggle' | chpasswd

RUN sed -i -e 's/^.\?PermitRootLogin.*/PermitRootLogin yes/' \
    -e 's/^.\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
    -e 's/^.\?PasswordAuthentication.*/PasswordAuthentication no/' \
    -e 's/^.\?UsePAM.*/UsePAM no/' \
    -e 's/^.\?LogLevel.*/LogLevel VERBOSE/' \
    -e 's:^.\?AuthorizedKeysFile.*:AuthorizedKeysFile /usr/lib/waggle/SSL/nodes/authorized_keys:' \
    /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

COPY register.sh /usr/lib/waggle/beehive-server/beehive-sshd/register.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
