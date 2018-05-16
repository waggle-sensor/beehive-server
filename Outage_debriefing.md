
# What Happened
As a very broad statement,the cause was an erroneous execution of a script that took actions to "harden" the system, overriding correct system setup with what the script thought it should be.

# What Caused it
A script that was produced by CIS, (Center for Information Security), a renowned leader in enterprises for security compliance and hardening (used by UChicago), develops scripts that "examine" a system, and compares the results to a specific set of values that CIS thinks is acceptable. This is called a workbench to CIS. Each workbench is designated for a specific system and the environment that it is run under. 

The next items are a two-fold issue. First,the CentOS workbench was downloaded from their portal, and was **supposed** to be pre-ran on my workstation, to make sure nothing bad would happen. It was executed in the wrong terminal window, thus causing the system to harden and degregate. Secondly, after a naming convention change in CIS, they no longer offer just the analyzer, it is now also a "remediation kit", which in addition to printing results of the analyzer, it now takes "corrective" action.

# Why it was ran
I was tasked with doing a thorough review of Beehive, including a security and port audit. To efficiently & effectively get this job done, I turned to this software to conduct the search on my behalf, and would present what it recommends to Raj and Pete, seeing how we wanted to move forward.Having used this software frequently in past roles, I knew it could give us a thorough review that would take me personally a while to construct.

# How it was fixed
After discoverying the issue, Max & Brad were engaged. I handed over what I ran to them, and they tried to reverse what had happened. Because of the complexity and thoroughness of the script, it was determined that a restore was our best option. After weighing our options, luckily, the NetApp that is the storage backing(storage backing==working to confirm this) to our VM had successfully taken a snapshot a couple hours before the mishap, resulting in a near-identical image of Beehive. A "bare-metal" VM was spun up, and the snapshot image was "injected" into it. 

Sean and Raj worked after Beehive was powered up to work out a couple bugs, including a possible race condition where Cassandra didn't want to start.

# Next Steps
Currently auditing and going through Beehive to see what the next plan of action is. 

## The Script in its entirety is below
```
#!/bin/bash
PROFILE=${1:-Level 1 - Server}

if [ "$PROFILE" = "Level 1 - Server" ] || [ "$PROFILE" = "Level 2 - Server" ]; then
  echo \*\*\*\* Executing Level 1 - Server profile remediation

  # Ensure mounting of cramfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ cramfs\ filesystems\ is\ disabled
  modprobe -n -v cramfs | grep "^install /bin/true$" || echo "install cramfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^cramfs\s" && rmmod cramfs

  # Ensure mounting of freevxfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ freevxfs\ filesystems\ is\ disabled
  modprobe -n -v freevxfs | grep "^install /bin/true$" || echo "install freevxfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^freevxfs\s" && rmmod freevxfs

  # Ensure mounting of jffs2 filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ jffs2\ filesystems\ is\ disabled
  modprobe -n -v jffs2 | grep "^install /bin/true$" || echo "install jffs2 /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^jffs2\s" && rmmod jffs2

  # Ensure mounting of hfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ hfs\ filesystems\ is\ disabled
  modprobe -n -v hfs | grep "^install /bin/true$" || echo "install hfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^hfs\s" && rmmod hfs

  # Ensure mounting of hfsplus filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ hfsplus\ filesystems\ is\ disabled
  modprobe -n -v hfsplus | grep "^install /bin/true$" || echo "install hfsplus /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^hfsplus\s" && rmmod hfsplus

  # Ensure mounting of squashfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ squashfs\ filesystems\ is\ disabled
  modprobe -n -v squashfs | grep "^install /bin/true$" || echo "install squashfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^squashfs\s" && rmmod squashfs

  # Ensure mounting of udf filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ udf\ filesystems\ is\ disabled
  modprobe -n -v udf | grep "^install /bin/true$" || echo "install udf /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^udf\s" && rmmod udf

  # Ensure mounting of FAT filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ FAT\ filesystems\ is\ disabled
  modprobe -n -v vfat | grep "^install /bin/true$" || echo "install vfat /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^vfat\s" && rmmod vfat

  # Ensure nodev option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /tmp\ partition
  echo Ensure\ nodev\ option\ set\ on\ /tmp\ partition not configured

  # Ensure nosuid option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /tmp\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /tmp\ partition not configured

  # Ensure noexec option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /tmp\ partition
  echo Ensure\ noexec\ option\ set\ on\ /tmp\ partition not configured

  # Ensure nodev option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ nodev\ option\ set\ on\ /var/tmp\ partition not configured

  # Ensure nosuid option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /var/tmp\ partition not configured

  # Ensure noexec option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ noexec\ option\ set\ on\ /var/tmp\ partition not configured

  # Ensure nodev option set on /home partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /home\ partition
  echo Ensure\ nodev\ option\ set\ on\ /home\ partition not configured

  # Ensure nodev option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ nodev\ option\ set\ on\ /dev/shm\ partition not configured

  # Ensure nosuid option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /dev/shm\ partition not configured

  # Ensure noexec option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ noexec\ option\ set\ on\ /dev/shm\ partition not configured

  # Ensure sticky bit is set on all world-writable directories
  echo
  echo \*\*\*\* Ensure\ sticky\ bit\ is\ set\ on\ all\ world-writable\ directories
  df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null | xargs chmod a+t

  # Disable Automounting
  echo
  echo \*\*\*\* Disable\ Automounting
  systemctl disable autofs.service

  # Ensure gpgcheck is globally activated
  echo
  echo \*\*\*\* Ensure\ gpgcheck\ is\ globally\ activated
  egrep -q "^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$" /etc/yum.conf && sed -ri "s/^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$/\1gpgcheck=1\2/" /etc/yum.conf || echo "gpgcheck=1" >> /etc/yum.conf
  for file in /etc/yum.repos.d/*; do
    egrep -q "^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$" $file && sed -ri "s/^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$/\1gpgcheck=1\2/" $file || echo "gpgcheck=1" >> $file
  done

  # Ensure AIDE is installed
  echo
  echo \*\*\*\* Ensure\ AIDE\ is\ installed
  rpm -q aide || yum -y install aide

  # Ensure filesystem integrity is regularly checked
  echo
  echo \*\*\*\* Ensure\ filesystem\ integrity\ is\ regularly\ checked
  (crontab -u root -l; crontab -u root -l | egrep -q "^0 5 \* \* \* /usr/sbin/aide --check$" || echo "0 5 * * * /usr/sbin/aide --check" ) | crontab -u root -

  # Ensure permissions on bootloader config are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ bootloader\ config\ are\ configured
  chmod g-r-w-x,o-r-w-x /boot/grub2/grub.cfg

  # Ensure bootloader password is set
  echo
  echo \*\*\*\* Ensure\ bootloader\ password\ is\ set
  echo Ensure\ bootloader\ password\ is\ set not configured.

  # Ensure authentication required for single user mode
  echo
  echo \*\*\*\* Ensure\ authentication\ required\ for\ single\ user\ mode
  egrep -q "^\s*ExecStart" /usr/lib/systemd/system/rescue.service && sed -ri "s/(^[[:space:]]*ExecStart[[:space:]]*=[[:space:]]*).*$/\1-\/bin\/sh -c \"\/sbin\/sulogin; \/usr\/bin\/systemctl --fail --no-block default\"/" /usr/lib/systemd/system/rescue.service || echo "ExecStart=-/bin/sh -c \"/sbin/sulogin; /usr/bin/systemctl --fail --no-block default\"" >> /usr/lib/systemd/system/rescue.service
  egrep -q "^\s*ExecStart" /usr/lib/systemd/system/emergency.service && sed -ri "s/(^[[:space:]]*ExecStart[[:space:]]*=[[:space:]]*).*$/\1-\/bin\/sh -c \"\/sbin\/sulogin; \/usr\/bin\/systemctl --fail --no-block default\"/" /usr/lib/systemd/system/emergency.service || echo "ExecStart=-/bin/sh -c \"/sbin/sulogin; /usr/bin/systemctl --fail --no-block default\"" >> /usr/lib/systemd/system/emergency.service

  # Ensure core dumps are restricted
  echo
  echo \*\*\*\* Ensure\ core\ dumps\ are\ restricted
  egrep -q "^(\s*)\*\s+hard\s+core\s+\S+(\s*#.*)?\s*$" /etc/security/limits.conf && sed -ri "s/^(\s*)\*\s+hard\s+core\s+\S+(\s*#.*)?\s*$/\1* hard core 0\2/" /etc/security/limits.conf || echo "* hard core 0" >> /etc/security/limits.conf
  egrep -q "^(\s*)fs.suid_dumpable\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)fs.suid_dumpable\s*=\s*\S+(\s*#.*)?\s*$/\1fs.suid_dumpable = 0\2/" /etc/sysctl.conf || echo "fs.suid_dumpable = 0" >> /etc/sysctl.conf

  # Ensure XD/NX support is enabled
  echo
  echo \*\*\*\* Ensure\ XD/NX\ support\ is\ enabled
  echo Ensure\ XD/NX\ support\ is\ enabled not configured.

  # Ensure address space layout randomization (ASLR) is enabled
  echo
  echo \*\*\*\* Ensure\ address\ space\ layout\ randomization\ \(ASLR\)\ is\ enabled
  egrep -q "^(\s*)kernel.randomize_va_space\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)kernel.randomize_va_space\s*=\s*\S+(\s*#.*)?\s*$/\1kernel.randomize_va_space = 2\2/" /etc/sysctl.conf || echo "kernel.randomize_va_space = 2" >> /etc/sysctl.conf

  # Ensure prelink is disabled
  echo
  echo \*\*\*\* Ensure\ prelink\ is\ disabled
  rpm -q prelink && yum -y remove prelink

  # Ensure message of the day is configured properly
  echo
  echo \*\*\*\* Ensure\ message\ of\ the\ day\ is\ configured\ properly
  sed -ri 's/(\\v|\\r|\\m|\\s)//g' /etc/motd

  # Ensure local login warning banner is configured properly
  echo
  echo \*\*\*\* Ensure\ local\ login\ warning\ banner\ is\ configured\ properly
  echo "Authorized uses only. All activity may be monitored and reported." > /etc/issue

  # Ensure remote login warning banner is configured properly
  echo
  echo \*\*\*\* Ensure\ remote\ login\ warning\ banner\ is\ configured\ properly
  echo "Authorized uses only. All activity may be monitored and reported." > /etc/issue.net

  # Ensure permissions on /etc/motd are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/motd\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/motd

  # Ensure permissions on /etc/issue are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/issue\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/issue

  # Ensure permissions on /etc/issue.net are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/issue.net\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/issue.net

  # Ensure GDM login banner is configured
  echo
  echo \*\*\*\* Ensure\ GDM\ login\ banner\ is\ configured
  echo Ensure\ GDM\ login\ banner\ is\ configured not configured.

  # Ensure chargen services are not enabled
  echo
  echo \*\*\*\* Ensure\ chargen\ services\ are\ not\ enabled
  chkconfig chargen off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure daytime services are not enabled
  echo
  echo \*\*\*\* Ensure\ daytime\ services\ are\ not\ enabled
  chkconfig daytime off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure discard services are not enabled
  echo
  echo \*\*\*\* Ensure\ discard\ services\ are\ not\ enabled
  chkconfig discard off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure echo services are not enabled
  echo
  echo \*\*\*\* Ensure\ echo\ services\ are\ not\ enabled
  chkconfig echo off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure time services are not enabled
  echo
  echo \*\*\*\* Ensure\ time\ services\ are\ not\ enabled
  chkconfig time off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure tftp server is not enabled
  echo
  echo \*\*\*\* Ensure\ tftp\ server\ is\ not\ enabled
  chkconfig tftp off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified
  systemctl disable tftp.socket.service

  # Ensure xinetd is not enabled
  echo
  echo \*\*\*\* Ensure\ xinetd\ is\ not\ enabled
  systemctl disable xinetd.service

  # Ensure time synchronization is in use
  echo
  echo \*\*\*\* Ensure\ time\ synchronization\ is\ in\ use
  rpm -q ntp || rpm -q chrony || yum -y install chrony

  # Ensure ntp is configured
  echo
  echo \*\*\*\* Ensure\ ntp\ is\ configured
  if rpm -q ntp >/dev/null; then
    egrep -q "^\s*restrict(\s+-4)?\s+default(\s+\S+)*(\s*#.*)?\s*$" /etc/ntp.conf && sed -ri "s/^(\s*)restrict(\s+-4)?\s+default(\s+[^[:space:]#]+)*(\s+#.*)?\s*$/\1restrict\2 default kod nomodify notrap nopeer noquery\4/" /etc/ntp.conf || echo "restrict default kod nomodify notrap nopeer noquery" >> /etc/ntp.conf 
    egrep -q "^\s*restrict\s+-6\s+default(\s+\S+)*(\s*#.*)?\s*$" /etc/ntp.conf && sed -ri "s/^(\s*)restrict\s+-6\s+default(\s+[^[:space:]#]+)*(\s+#.*)?\s*$/\1restrict -6 default kod nomodify notrap nopeer noquery\3/" /etc/ntp.conf || echo "restrict -6 default kod nomodify notrap nopeer noquery" >> /etc/ntp.conf 
    egrep -q "^(\s*)OPTIONS\s*=\s*\"(([^\"]+)?-u\s[^[:space:]\"]+([^\"]+)?|([^\"]+))\"(\s*#.*)?\s*$" /etc/sysconfig/ntpd && sed -ri '/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/ {/^(\s*)OPTIONS\s*=\s*\"[^\"]*-u\s+\S+[^\"]*\"(\s*#.*)?\s*$/! s/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/\1OPTIONS=\"\2 -u ntp:ntp\"\3/ }' /etc/sysconfig/ntpd && sed -ri "s/^(\s*)OPTIONS\s*=\s*\"([^\"]+\s+)?-u\s[^[:space:]\"]+(\s+[^\"]+)?\"(\s*#.*)?\s*$/\1OPTIONS=\"\2\-u ntp:ntp\3\"\4/" /etc/sysconfig/ntpd || echo "OPTIONS=\"-u ntp:ntp\"" >> /etc/sysconfig/ntpd
    echo Ensure ntp is configured - server not configured.
  fi

  # Ensure chrony is configured
  echo
  echo \*\*\*\* Ensure\ chrony\ is\ configured
  if rpm -q chrony >/dev/null; then
    egrep -q "^(\s*)OPTIONS\s*=\s*\"(([^\"]+)?-u\s[^[:space:]\"]+([^\"]+)?|([^\"]+))\"(\s*#.*)?\s*$" /etc/sysconfig/chronyd && sed -ri '/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/ {/^(\s*)OPTIONS\s*=\s*\"[^\"]*-u\s+\S+[^\"]*\"(\s*#.*)?\s*$/! s/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/\1OPTIONS=\"\2 -u chrony\"\3/ }' /etc/sysconfig/chronyd && sed -ri "s/^(\s*)OPTIONS\s*=\s*\"([^\"]+\s+)?-u\s[^[:space:]\"]+(\s+[^\"]+)?\"(\s*#.*)?\s*$/\1OPTIONS=\"\2\-u chrony\3\"\4/" /etc/sysconfig/chronyd || echo "OPTIONS=\"-u chrony\"" >> /etc/sysconfig/chronyd
    echo Ensure chrony is configured - server not configured.
  fi

  # Ensure X Window System is not installed
  echo
  echo \*\*\*\* Ensure\ X\ Window\ System\ is\ not\ installed
  yum -y remove xorg-x11*

  # Ensure Avahi Server is not enabled
  echo
  echo \*\*\*\* Ensure\ Avahi\ Server\ is\ not\ enabled
  systemctl disable avahi-daemon.service

  # Ensure CUPS is not enabled
  echo
  echo \*\*\*\* Ensure\ CUPS\ is\ not\ enabled
  systemctl disable cups.service

  # Ensure DHCP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ DHCP\ Server\ is\ not\ enabled
  systemctl disable dhcpd.service

  # Ensure LDAP server is not enabled
  echo
  echo \*\*\*\* Ensure\ LDAP\ server\ is\ not\ enabled
  systemctl disable slapd.service

  # Ensure NFS and RPC are not enabled
  echo
  echo \*\*\*\* Ensure\ NFS\ and\ RPC\ are\ not\ enabled
  systemctl disable nfs.service
  systemctl disable rpcbind.service

  # Ensure DNS Server is not enabled
  echo
  echo \*\*\*\* Ensure\ DNS\ Server\ is\ not\ enabled
  systemctl disable named.service

  # Ensure FTP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ FTP\ Server\ is\ not\ enabled
  systemctl disable vsftpd.service

  # Ensure HTTP server is not enabled
  echo
  echo \*\*\*\* Ensure\ HTTP\ server\ is\ not\ enabled
  systemctl disable htttpd.service

  # Ensure IMAP and POP3 server is not enabled
  echo
  echo \*\*\*\* Ensure\ IMAP\ and\ POP3\ server\ is\ not\ enabled
  systemctl disable dovecot.service

  # Ensure Samba is not enabled
  echo
  echo \*\*\*\* Ensure\ Samba\ is\ not\ enabled
  systemctl disable smb.service

  # Ensure HTTP Proxy Server is not enabled
  echo
  echo \*\*\*\* Ensure\ HTTP\ Proxy\ Server\ is\ not\ enabled
  systemctl disable squid.service

  # Ensure SNMP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ SNMP\ Server\ is\ not\ enabled
  systemctl disable snmpd.service

  # Ensure mail transfer agent is configured for local-only mode
  echo
  echo \*\*\*\* Ensure\ mail\ transfer\ agent\ is\ configured\ for\ local-only\ mode
  echo Ensure\ mail\ transfer\ agent\ is\ configured\ for\ local-only\ mode Linux custom object not configured.

  # Ensure NIS Server is not enabled
  echo
  echo \*\*\*\* Ensure\ NIS\ Server\ is\ not\ enabled
  systemctl disable ypserv.service

  # Ensure rsh server is not enabled
  echo
  echo \*\*\*\* Ensure\ rsh\ server\ is\ not\ enabled
  systemctl disable rsh.socket.service
  systemctl disable rlogin.socket.service
  systemctl disable rexec.socket.service

  # Ensure telnet server is not enabled
  echo
  echo \*\*\*\* Ensure\ telnet\ server\ is\ not\ enabled
  systemctl disable telnet.socket.service

  # Ensure rsync service is not enabled
  echo
  echo \*\*\*\* Ensure\ rsync\ service\ is\ not\ enabled
  systemctl disable rsyncd.service

  # Ensure talk server is not enabled
  echo
  echo \*\*\*\* Ensure\ talk\ server\ is\ not\ enabled
  systemctl disable ntalk.service

  # Ensure NIS Client is not installed
  echo
  echo \*\*\*\* Ensure\ NIS\ Client\ is\ not\ installed
  rpm -q ypbind && yum -y remove ypbind

  # Ensure rsh client is not installed
  echo
  echo \*\*\*\* Ensure\ rsh\ client\ is\ not\ installed
  rpm -q rsh && yum -y remove rsh

  # Ensure talk client is not installed
  echo
  echo \*\*\*\* Ensure\ talk\ client\ is\ not\ installed
  rpm -q talk && yum -y remove talk

  # Ensure telnet client is not installed
  echo
  echo \*\*\*\* Ensure\ telnet\ client\ is\ not\ installed
  rpm -q telnet && yum -y remove telnet

  # Ensure LDAP client is not installed
  echo
  echo \*\*\*\* Ensure\ LDAP\ client\ is\ not\ installed
  rpm -q openldap-clients && yum -y remove openldap-clients

  # Ensure IP forwarding is disabled
  echo
  echo \*\*\*\* Ensure\ IP\ forwarding\ is\ disabled
  egrep -q "^(\s*)net.ipv4.ip_forward\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.ip_forward\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.ip_forward = 0\2/" /etc/sysctl.conf || echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf

  # Ensure packet redirect sending is disabled
  echo
  echo \*\*\*\* Ensure\ packet\ redirect\ sending\ is\ disabled
  egrep -q "^(\s*)net.ipv4.conf.all.send_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.send_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.send_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.send_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.send_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.send_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.send_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.send_redirects = 0" >> /etc/sysctl.conf

  # Ensure source routed packets are not accepted
  echo
  echo \*\*\*\* Ensure\ source\ routed\ packets\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_source_route = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_source_route = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.accept_source_route = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.accept_source_route = 0" >> /etc/sysctl.conf

  # Ensure ICMP redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ ICMP\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf

  # Ensure secure ICMP redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ secure\ ICMP\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.secure_redirects = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.secure_redirects = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.secure_redirects = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.secure_redirects = 1" >> /etc/sysctl.conf

  # Ensure suspicious packets are logged
  echo
  echo \*\*\*\* Ensure\ suspicious\ packets\ are\ logged
  egrep -q "^(\s*)net.ipv4.conf.all.log_martians\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.log_martians\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.log_martians = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.log_martians = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.log_martians\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.log_martians\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.log_martians = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.log_martians = 1" >> /etc/sysctl.conf

  # Ensure broadcast ICMP requests are ignored
  echo
  echo \*\*\*\* Ensure\ broadcast\ ICMP\ requests\ are\ ignored
  egrep -q "^(\s*)net.ipv4.icmp_echo_ignore_broadcasts\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.icmp_echo_ignore_broadcasts\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.icmp_echo_ignore_broadcasts = 1\2/" /etc/sysctl.conf || echo "net.ipv4.icmp_echo_ignore_broadcasts = 1" >> /etc/sysctl.conf

  # Ensure bogus ICMP responses are ignored
  echo
  echo \*\*\*\* Ensure\ bogus\ ICMP\ responses\ are\ ignored
  egrep -q "^(\s*)net.ipv4.icmp_ignore_bogus_error_responses\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.icmp_ignore_bogus_error_responses\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.icmp_ignore_bogus_error_responses = 1\2/" /etc/sysctl.conf || echo "net.ipv4.icmp_ignore_bogus_error_responses = 1" >> /etc/sysctl.conf

  # Ensure Reverse Path Filtering is enabled
  echo
  echo \*\*\*\* Ensure\ Reverse\ Path\ Filtering\ is\ enabled
  egrep -q "^(\s*)net.ipv4.conf.all.rp_filter\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.rp_filter\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.rp_filter = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.rp_filter = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.rp_filter\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.rp_filter\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.rp_filter = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.rp_filter = 1" >> /etc/sysctl.conf

  # Ensure TCP SYN Cookies is enabled
  echo
  echo \*\*\*\* Ensure\ TCP\ SYN\ Cookies\ is\ enabled
  egrep -q "^(\s*)net.ipv4.tcp_syncookies\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.tcp_syncookies\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.tcp_syncookies = 1\2/" /etc/sysctl.conf || echo "net.ipv4.tcp_syncookies = 1" >> /etc/sysctl.conf

  # Ensure IPv6 router advertisements are not accepted
  echo
  echo \*\*\*\* Ensure\ IPv6\ router\ advertisements\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv6.conf.all.accept_ra\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.all.accept_ra\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.all.accept_ra = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.all.accept_ra = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv6.conf.default.accept_ra\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.default.accept_ra\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.default.accept_ra = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.default.accept_ra = 0" >> /etc/sysctl.conf

  # Ensure IPv6 redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ IPv6\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv6.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv6.conf.default.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.default.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.default.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.default.accept_redirects = 0" >> /etc/sysctl.conf

  # Ensure IPv6 is disabled
  echo
  echo \*\*\*\* Ensure\ IPv6\ is\ disabled
  echo Ensure\ IPv6\ is\ disabled not configured.

  # Ensure TCP Wrappers is installed
  echo
  echo \*\*\*\* Ensure\ TCP\ Wrappers\ is\ installed
  rpm -q tcp_wrappers || yum -y install tcp_wrappers
  rpm -q tcp_wrappers-libs || yum -y install tcp_wrappers-libs

  # Ensure /etc/hosts.allow is configured
  echo
  echo \*\*\*\* Ensure\ /etc/hosts.allow\ is\ configured
  touch /etc/hosts.allow

  # Ensure /etc/hosts.deny is configured
  echo
  echo \*\*\*\* Ensure\ /etc/hosts.deny\ is\ configured
  echo Ensure\ /etc/hosts.deny\ is\ configured not configured.

  # Ensure permissions on /etc/hosts.allow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/hosts.allow\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/hosts.allow

  # Ensure permissions on /etc/hosts.deny are 644
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/hosts.deny\ are\ 644
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/hosts.deny

  # Ensure DCCP is disabled
  echo
  echo \*\*\*\* Ensure\ DCCP\ is\ disabled
  modprobe -n -v dccp | grep "^install /bin/true$" || echo "install dccp /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^dccp\s" && rmmod dccp

  # Ensure SCTP is disabled
  echo
  echo \*\*\*\* Ensure\ SCTP\ is\ disabled
  modprobe -n -v sctp | grep "^install /bin/true$" || echo "install sctp /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^sctp\s" && rmmod sctp

  # Ensure RDS is disabled
  echo
  echo \*\*\*\* Ensure\ RDS\ is\ disabled
  modprobe -n -v rds | grep "^install /bin/true$" || echo "install rds /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^rds\s" && rmmod rds

  # Ensure TIPC is disabled
  echo
  echo \*\*\*\* Ensure\ TIPC\ is\ disabled
  modprobe -n -v tipc | grep "^install /bin/true$" || echo "install tipc /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^tipc\s" && rmmod tipc

  # Ensure iptables is installed
  echo
  echo \*\*\*\* Ensure\ iptables\ is\ installed
  rpm -q iptables || yum -y install iptables

  # Ensure default deny firewall policy
  echo
  echo \*\*\*\* Ensure\ default\ deny\ firewall\ policy
  echo Ensure\ default\ deny\ firewall\ policy not configured.

  # Ensure loopback traffic is configured
  echo
  echo \*\*\*\* Ensure\ loopback\ traffic\ is\ configured
  echo Ensure\ loopback\ traffic\ is\ configured not configured.

  # Ensure firewall rules exist for all open ports
  echo
  echo \*\*\*\* Ensure\ firewall\ rules\ exist\ for\ all\ open\ ports
  echo Ensure\ firewall\ rules\ exist\ for\ all\ open\ ports not configured.

  # Ensure rsyslog Service is enabled
  echo
  echo \*\*\*\* Ensure\ rsyslog\ Service\ is\ enabled
  rpm -q rsyslog && systemctl enable rsyslog.service

  # Ensure rsyslog default file permissions configured
  echo
  echo \*\*\*\* Ensure\ rsyslog\ default\ file\ permissions\ configured
  echo Ensure\ rsyslog\ default\ file\ permissions\ configured not configured.

  # Ensure rsyslog is configured to send logs to a remote log host
  echo
  echo \*\*\*\* Ensure\ rsyslog\ is\ configured\ to\ send\ logs\ to\ a\ remote\ log\ host
  echo Ensure\ rsyslog\ is\ configured\ to\ send\ logs\ to\ a\ remote\ log\ host not configured.

  # Ensure syslog-ng service is enabled
  echo
  echo \*\*\*\* Ensure\ syslog-ng\ service\ is\ enabled
  rpm -q syslog-ng && systemctl enable syslog-ng.service

  # Ensure syslog-ng default file permissions configured
  echo
  echo \*\*\*\* Ensure\ syslog-ng\ default\ file\ permissions\ configured
  echo Ensure\ syslog-ng\ default\ file\ permissions\ configured not configured.

  # Ensure rsyslog or syslog-ng is installed
  echo
  echo \*\*\*\* Ensure\ rsyslog\ or\ syslog-ng\ is\ installed
  rpm -q rsyslog || rpm -q syslog-ng || yum -y install rsyslog

  # Ensure permissions on all logfiles are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ all\ logfiles\ are\ configured
  chmod -R g-w-x,o-r-w-x /var/log/.*

  # Ensure cron daemon is enabled
  echo
  echo \*\*\*\* Ensure\ cron\ daemon\ is\ enabled
  systemctl enable crond.service

  # Ensure permissions on /etc/crontab are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/crontab\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/crontab

  # Ensure permissions on /etc/cron.hourly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.hourly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.hourly

  # Ensure permissions on /etc/cron.daily are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.daily\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.daily

  # Ensure permissions on /etc/cron.weekly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.weekly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.weekly

  # Ensure permissions on /etc/cron.monthly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.monthly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.monthly

  # Ensure permissions on /etc/cron.d are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.d\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.d

  # Ensure at/cron is restricted to authorized users
  echo
  echo \*\*\*\* Ensure\ at/cron\ is\ restricted\ to\ authorized\ users
  rm /etc/cron.deny
  rm /etc/at.deny
  touch /etc/cron.allow
  touch /etc/at.allow
  chmod g-r-w-x,o-r-w-x /etc/cron.allow
  chmod g-r-w-x,o-r-w-x /etc/at.allow

  # Ensure permissions on /etc/ssh/sshd_config are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/ssh/sshd_config\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/ssh/sshd_config

  # Ensure SSH Protocol is set to 2
  echo
  echo \*\*\*\* Ensure\ SSH\ Protocol\ is\ set\ to\ 2
  egrep -q "^(\s*)Protocol\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Protocol\s+\S+(\s*#.*)?\s*$/\1Protocol 2\2/" /etc/ssh/sshd_config || echo "Protocol 2" >> /etc/ssh/sshd_config

  # Ensure SSH LogLevel is set to INFO
  echo
  echo \*\*\*\* Ensure\ SSH\ LogLevel\ is\ set\ to\ INFO
  egrep -q "^(\s*)LogLevel\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)LogLevel\s+\S+(\s*#.*)?\s*$/\1LogLevel INFO\2/" /etc/ssh/sshd_config || echo "LogLevel INFO" >> /etc/ssh/sshd_config

  # Ensure SSH X11 forwarding is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ X11\ forwarding\ is\ disabled
  egrep -q "^(\s*)X11Forwarding\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)X11Forwarding\s+\S+(\s*#.*)?\s*$/\1X11Forwarding no\2/" /etc/ssh/sshd_config || echo "X11Forwarding no" >> /etc/ssh/sshd_config

  # Ensure SSH MaxAuthTries is set to 4 or less
  echo
  echo \*\*\*\* Ensure\ SSH\ MaxAuthTries\ is\ set\ to\ 4\ or\ less
  egrep -q "^(\s*)MaxAuthTries\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)MaxAuthTries\s+\S+(\s*#.*)?\s*$/\1MaxAuthTries 4\2/" /etc/ssh/sshd_config || echo "MaxAuthTries 4" >> /etc/ssh/sshd_config

  # Ensure SSH IgnoreRhosts is enabled
  echo
  echo \*\*\*\* Ensure\ SSH\ IgnoreRhosts\ is\ enabled
  egrep -q "^(\s*)IgnoreRhosts\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)IgnoreRhosts\s+\S+(\s*#.*)?\s*$/\1IgnoreRhosts yes\2/" /etc/ssh/sshd_config || echo "IgnoreRhosts yes" >> /etc/ssh/sshd_config

  # Ensure SSH HostbasedAuthentication is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ HostbasedAuthentication\ is\ disabled
  egrep -q "^(\s*)HostbasedAuthentication\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)HostbasedAuthentication\s+\S+(\s*#.*)?\s*$/\1HostbasedAuthentication no\2/" /etc/ssh/sshd_config || echo "HostbasedAuthentication no" >> /etc/ssh/sshd_config

  # Ensure SSH root login is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ root\ login\ is\ disabled
  egrep -q "^(\s*)PermitRootLogin\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitRootLogin\s+\S+(\s*#.*)?\s*$/\1PermitRootLogin no\2/" /etc/ssh/sshd_config || echo "PermitRootLogin no" >> /etc/ssh/sshd_config

  # Ensure SSH PermitEmptyPasswords is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ PermitEmptyPasswords\ is\ disabled
  egrep -q "^(\s*)PermitEmptyPasswords\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitEmptyPasswords\s+\S+(\s*#.*)?\s*$/\1PermitEmptyPasswords no\2/" /etc/ssh/sshd_config || echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config

  # Ensure SSH PermitUserEnvironment is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ PermitUserEnvironment\ is\ disabled
  egrep -q "^(\s*)PermitUserEnvironment\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitUserEnvironment\s+\S+(\s*#.*)?\s*$/\1PermitUserEnvironment no\2/" /etc/ssh/sshd_config || echo "PermitUserEnvironment no" >> /etc/ssh/sshd_config

  # Ensure only approved ciphers are used
  echo
  echo \*\*\*\* Ensure\ only\ approved\ ciphers\ are\ used
  egrep -q "^(\s*)Ciphers\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Ciphers\s+\S+(\s*#.*)?\s*$/\Ciphers aes256-ctr,aes192-ctr,aes128-ctr\2/" /etc/ssh/sshd_config || echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr" >> /etc/ssh/sshd_config

  # Ensure only approved MAC algorithms are used
  echo
  echo \*\*\*\* Ensure\ only\ approved\ MAC\ algorithms\ are\ used
  egrep -q "^(\s*)MACs\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)MACs\s+\S+(\s*#.*)?\s*$/\MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com\2/" /etc/ssh/sshd_config || echo "MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com" >> /etc/ssh/sshd_config

  # Ensure SSH Idle Timeout Interval is configured
  echo
  echo \*\*\*\* Ensure\ SSH\ Idle\ Timeout\ Interval\ is\ configured
  egrep -q "^(\s*)ClientAliveInterval\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)ClientAliveInterval\s+\S+(\s*#.*)?\s*$/\1ClientAliveInterval 300\2/" /etc/ssh/sshd_config || echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
  egrep -q "^(\s*)ClientAliveCountMax\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)ClientAliveCountMax\s+\S+(\s*#.*)?\s*$/\1ClientAliveCountMax 3\2/" /etc/ssh/sshd_config || echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config

  # Ensure SSH LoginGraceTime is set to one minute or less
  echo
  echo \*\*\*\* Ensure\ SSH\ LoginGraceTime\ is\ set\ to\ one\ minute\ or\ less
  egrep -q "^(\s*)LoginGraceTime\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)LoginGraceTime\s+\S+(\s*#.*)?\s*$/\1LoginGraceTime 60\2/" /etc/ssh/sshd_config || echo "LoginGraceTime 60" >> /etc/ssh/sshd_config

  # Ensure SSH access is limited
  echo
  echo \*\*\*\* Ensure\ SSH\ access\ is\ limited
  echo Ensure\ SSH\ access\ is\ limited not configured.

  # Ensure SSH warning banner is configured
  echo
  echo \*\*\*\* Ensure\ SSH\ warning\ banner\ is\ configured
  egrep -q "^(\s*)Banner\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Banner\s+\S+(\s*#.*)?\s*$/\1Banner \/etc\/issue.net\2/" /etc/ssh/sshd_config || echo "Banner /etc/issue.net" >> /etc/ssh/sshd_config

  # Ensure password creation requirements are configured
  echo
  echo \*\*\*\* Ensure\ password\ creation\ requirements\ are\ configured
  egrep -q "^(\s*)minlen\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)minlen\s*=\s*\S+(\s*#.*)?\s*$/\minlen=14\2/" /etc/security/pwquality.conf || echo "minlen=14" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)dcredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)dcredit\s*=\s*\S+(\s*#.*)?\s*$/\dcredit=-1\2/" /etc/security/pwquality.conf || echo "dcredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)ucredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)ucredit\s*=\s*\S+(\s*#.*)?\s*$/\ucredit=-1\2/" /etc/security/pwquality.conf || echo "ucredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)ocredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)ocredit\s*=\s*\S+(\s*#.*)?\s*$/\ocredit=-1\2/" /etc/security/pwquality.conf || echo "ocredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)lcredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)lcredit\s*=\s*\S+(\s*#.*)?\s*$/\lcredit=-1\2/" /etc/security/pwquality.conf || echo "lcredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^\s*password\s+requisite\s+pam_pwquality.so\s+" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+try_first_pass)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1try_first_pass \2/ }' /etc/pam.d/system-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+retry=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1retry=3 \2/ }' /etc/pam.d/system-auth && sed -ri 's/(^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*\s+)retry=[0-9]+(\s+.*)?$/\1retry=3\3/' /etc/pam.d/system-auth || echo Ensure\ password\ creation\ requirements\ are\ configured - /etc/pam.d/system-auth not configured.
  egrep -q "^\s*password\s+requisite\s+pam_pwquality.so\s+" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+try_first_pass)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1try_first_pass \2/ }' /etc/pam.d/password-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+retry=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1retry=3 \2/ }' /etc/pam.d/password-auth && sed -ri 's/(^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*\s+)retry=[0-9]+(\s+.*)?$/\1retry=3\3/' /etc/pam.d/password-auth || echo Ensure\ password\ creation\ requirements\ are\ configured - /etc/pam.d/password-auth not configured.

  # Ensure lockout for failed password attempts is configured
  echo
  echo \*\*\*\* Ensure\ lockout\ for\ failed\ password\ attempts\ is\ configured
  echo Ensure\ lockout\ for\ failed\ password\ attempts\ is\ configured not configured.

  # Ensure password reuse is limited
  echo
  echo \*\*\*\* Ensure\ password\ reuse\ is\ limited
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so(\s+.*)$" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+remember=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1remember=5 \2/ }' /etc/pam.d/system-auth && sed -ri 's/(^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*\s+)remember=[0-9]+(\s+.*)?$/\1remember=5\3/' /etc/pam.d/system-auth || echo Ensure\ password\ reuse\ is\ limited - /etc/pam.d/system-auth not configured.
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so(\s+.*)$" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+remember=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1remember=5 \2/ }' /etc/pam.d/password-auth && sed -ri 's/(^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*\s+)remember=[0-9]+(\s+.*)?$/\1remember=5\3/' /etc/pam.d/password-auth || echo Ensure\ password\ reuse\ is\ limited - /etc/pam.d/password-auth not configured.

  # Ensure password hashing algorithm is SHA-512
  echo
  echo \*\*\*\* Ensure\ password\ hashing\ algorithm\ is\ SHA-512
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so\s+" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+sha512)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1sha512 \2/ }' /etc/pam.d/system-auth || echo Ensure\ password\ hashing\ algorithm\ is\ SHA-512 - /etc/pam.d/password-auth not configured.
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so\s+" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+sha512)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1sha512 \2/ }' /etc/pam.d/password-auth || echo Ensure\ password\ hashing\ algorithm\ is\ SHA-512 - /etc/pam.d/password-auth not configured.

  # Ensure password expiration is 90 days or less
  echo
  echo \*\*\*\* Ensure\ password\ expiration\ is\ 90\ days\ or\ less
  egrep -q "^(\s*)PASS_MAX_DAYS\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_MAX_DAYS\s+\S+(\s*#.*)?\s*$/\PASS_MAX_DAYS 90\2/" /etc/login.defs || echo "PASS_MAX_DAYS 90" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --maxdays 90

  # Ensure minimum days between password changes is 7 or more
  echo
  echo \*\*\*\* Ensure\ minimum\ days\ between\ password\ changes\ is\ 7\ or\ more
  egrep -q "^(\s*)PASS_MIN_DAYS\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_MIN_DAYS\s+\S+(\s*#.*)?\s*$/\PASS_MIN_DAYS 7\2/" /etc/login.defs || echo "PASS_MIN_DAYS 7" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --mindays 7

  # Ensure password expiration warning days is 7 or more
  echo
  echo \*\*\*\* Ensure\ password\ expiration\ warning\ days\ is\ 7\ or\ more
  egrep -q "^(\s*)PASS_WARN_AGE\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_WARN_AGE\s+\S+(\s*#.*)?\s*$/\PASS_WARN_AGE 7\2/" /etc/login.defs || echo "PASS_WARN_AGE 7" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --warndays 7

  # Ensure inactive password lock is 30 days or less
  echo
  echo \*\*\*\* Ensure\ inactive\ password\ lock\ is\ 30\ days\ or\ less
  useradd -D -f 30
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --inactive 30

  # Ensure system accounts are non-login
  echo
  echo \*\*\*\* Ensure\ system\ accounts\ are\ non-login
  for user in `awk -F: '($3 < 1000) {print $1 }' /etc/passwd`; do
  if [ $user != "root" ]
  then
    /usr/sbin/usermod -L $user
    if [ $user != "sync" ] && [ $user != "shutdown" ] && [ $user != "halt" ]
    then
      /usr/sbin/usermod -s /sbin/nologin $user
    fi
  fi
done


  # Ensure default group for the root account is GID 0
  echo
  echo \*\*\*\* Ensure\ default\ group\ for\ the\ root\ account\ is\ GID\ 0
  usermod -g 0 root

  # Ensure default user umask is 027 or more restrictive
  echo
  echo \*\*\*\* Ensure\ default\ user\ umask\ is\ 027\ or\ more\ restrictive
  egrep -q "^(\s*)umask\s+\S+(\s*#.*)?\s*$" /etc/bashrc && sed -ri "s/^(\s*)umask\s+\S+(\s*#.*)?\s*$/\1umask 077\2/" /etc/bashrc || echo "umask 077" >> /etc/bashrc
  egrep -q "^(\s*)umask\s+\S+(\s*#.*)?\s*$" /etc/profile && sed -ri "s/^(\s*)umask\s+\S+(\s*#.*)?\s*$/\1umask 077\2/" /etc/profile || echo "umask 077" >> /etc/profile

  # Ensure access to the su command is restricted
  echo
  echo \*\*\*\* Ensure\ access\ to\ the\ su\ command\ is\ restricted
  egrep -q "^\s*auth\s+required\s+pam_wheel.so(\s+.*)?$" /etc/pam.d/su && sed -ri '/^\s*auth\s+required\s+pam_wheel.so(\s+.*)?$/ { /^\s*auth\s+required\s+pam_wheel.so(\s+\S+)*(\s+use_uid)(\s+.*)?$/! s/^(\s*auth\s+required\s+pam_wheel.so)(\s+.*)?$/\1 use_uid\2/ }' /etc/pam.d/su || echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su

  # Ensure permissions on /etc/passwd are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/passwd\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/passwd

  # Ensure permissions on /etc/shadow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/shadow\ are\ configured
  chmod -t,u-x-s,g-w-x-s,o-r-w-x /etc/shadow

  # Ensure permissions on /etc/group are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/group\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/group

  # Ensure permissions on /etc/gshadow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/gshadow\ are\ configured
  chmod -t,u-x-s,g-w-x-s,o-r-w-x /etc/gshadow

  # Ensure permissions on /etc/passwd- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/passwd-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/passwd-

  # Ensure permissions on /etc/shadow- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/shadow-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/shadow-

  # Ensure permissions on /etc/group- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/group-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/group-

  # Ensure permissions on /etc/gshadow- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/gshadow-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/gshadow-

  # Ensure no world writable files exist
  echo
  echo \*\*\*\* Ensure\ no\ world\ writable\ files\ exist
  echo Ensure\ no\ world\ writable\ files\ exist Linux custom object not configured.

  # Ensure no unowned files or directories exist
  echo
  echo \*\*\*\* Ensure\ no\ unowned\ files\ or\ directories\ exist
  echo Ensure\ no\ unowned\ files\ or\ directories\ exist Linux custom object not configured.

  # Ensure no ungrouped files or directories exist
  echo
  echo \*\*\*\* Ensure\ no\ ungrouped\ files\ or\ directories\ exist
  echo Ensure\ no\ ungrouped\ files\ or\ directories\ exist Linux custom object not configured.

  # Ensure password fields are not empty
  echo
  echo \*\*\*\* Ensure\ password\ fields\ are\ not\ empty
  echo Ensure\ password\ fields\ are\ not\ empty not configured.

  # Ensure no legacy &quot;+&quot; entries exist in /etc/passwd
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/passwd
  sed -ri '/^\+:.*$/ d' /etc/passwd

  # Ensure no legacy &quot;+&quot; entries exist in /etc/shadow
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/shadow
  sed -ri '/^\+:.*$/ d' /etc/shadow

  # Ensure no legacy &quot;+&quot; entries exist in /etc/group
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/group
  sed -ri '/^\+:.*$/ d' /etc/group

  # Ensure root is the only UID 0 account
  echo
  echo \*\*\*\* Ensure\ root\ is\ the\ only\ UID\ 0\ account
  echo Ensure\ root\ is\ the\ only\ UID\ 0\ account not configured.

  # Ensure root PATH Integrity
  echo
  echo \*\*\*\* Ensure\ root\ PATH\ Integrity
  echo Ensure\ root\ PATH\ Integrity Linux custom object not configured.

  # Ensure all users' home directories exist
  echo
  echo \*\*\*\* Ensure\ all\ users\'\ home\ directories\ exist
  echo Ensure\ all\ users\'\ home\ directories\ exist Linux custom object not configured.

  # Ensure users' home directories permissions are 750 or more restrictive
  echo
  echo \*\*\*\* Ensure\ users\'\ home\ directories\ permissions\ are\ 750\ or\ more\ restrictive
  echo Ensure\ users\'\ home\ directories\ permissions\ are\ 750\ or\ more\ restrictive Linux custom object not configured.

  # Ensure users own their home directories
  echo
  echo \*\*\*\* Ensure\ users\ own\ their\ home\ directories
  echo Ensure\ users\ own\ their\ home\ directories not configured.

  # Ensure users' dot files are not group or world writable
  echo
  echo \*\*\*\* Ensure\ users\'\ dot\ files\ are\ not\ group\ or\ world\ writable
  echo Ensure\ users\'\ dot\ files\ are\ not\ group\ or\ world\ writable Linux custom object not configured.

  # Ensure no users have .forward files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .forward\ files
  echo Ensure\ no\ users\ have\ .forward\ files Linux custom object not configured.

  # Ensure no users have .netrc files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .netrc\ files
  echo Ensure\ no\ users\ have\ .netrc\ files Linux custom object not configured.

  # Ensure users' .netrc Files are not group or world accessible
  echo
  echo \*\*\*\* Ensure\ users\'\ .netrc\ Files\ are\ not\ group\ or\ world\ accessible
  echo Ensure\ users\'\ .netrc\ Files\ are\ not\ group\ or\ world\ accessible Linux custom object not configured.

  # Ensure no users have .rhosts files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .rhosts\ files
  echo Ensure\ no\ users\ have\ .rhosts\ files Linux custom object not configured.

  # Ensure all groups in /etc/passwd exist in /etc/group
  echo
  echo \*\*\*\* Ensure\ all\ groups\ in\ /etc/passwd\ exist\ in\ /etc/group
  echo Ensure\ all\ groups\ in\ /etc/passwd\ exist\ in\ /etc/group Linux custom object not configured.

  # Ensure no duplicate UIDs exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ UIDs\ exist
  echo Ensure\ no\ duplicate\ UIDs\ exist Linux custom object not configured.

  # Ensure no duplicate GIDs exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ GIDs\ exist
  echo Ensure\ no\ duplicate\ GIDs\ exist Linux custom object not configured.

  # Ensure no duplicate user names exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ user\ names\ exist
  echo Ensure\ no\ duplicate\ user\ names\ exist Linux custom object not configured.

  # Ensure no duplicate group names exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ group\ names\ exist
  echo Ensure\ no\ duplicate\ group\ names\ exist Linux custom object not configured.
fi

if [ "$PROFILE" = "Level 2 - Server" ]; then
  echo \*\*\*\* Executing Level 2 - Server profile remediation

  # Ensure separate partition exists for /tmp
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /tmp
  echo Ensure\ separate\ partition\ exists\ for\ /tmp not configured.

  # Ensure separate partition exists for /var
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var
  echo Ensure\ separate\ partition\ exists\ for\ /var not configured.

  # Ensure separate partition exists for /var/tmp
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/tmp
  echo Ensure\ separate\ partition\ exists\ for\ /var/tmp not configured.

  # Ensure separate partition exists for /var/log
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/log
  echo Ensure\ separate\ partition\ exists\ for\ /var/log not configured.

  # Ensure separate partition exists for /var/log/audit
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/log/audit
  echo Ensure\ separate\ partition\ exists\ for\ /var/log/audit not configured.

  # Ensure separate partition exists for /home
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /home
  echo Ensure\ separate\ partition\ exists\ for\ /home not configured.

  # Ensure SELinux is not disabled in bootloader configuration
  echo
  echo \*\*\*\* Ensure\ SELinux\ is\ not\ disabled\ in\ bootloader\ configuration
  echo Ensure\ SELinux\ is\ not\ disabled\ in\ bootloader\ configuration not configured.

  # Ensure the SELinux state is enforcing
  echo
  echo \*\*\*\* Ensure\ the\ SELinux\ state\ is\ enforcing
  echo Ensure\ the\ SELinux\ state\ is\ enforcing not configured.

  # Ensure SELinux policy is configured
  echo
  echo \*\*\*\* Ensure\ SELinux\ policy\ is\ configured
  echo Ensure\ SELinux\ policy\ is\ configured not configured.

  # Ensure SETroubleshoot is not installed
  echo
  echo \*\*\*\* Ensure\ SETroubleshoot\ is\ not\ installed
  rpm -q setroubleshoot && yum -y remove setroubleshoot

  # Ensure the MCS Translation Service (mcstrans) is not installed
  echo
  echo \*\*\*\* Ensure\ the\ MCS\ Translation\ Service\ \(mcstrans\)\ is\ not\ installed
  rpm -q mcstrans && yum -y remove mcstrans

  # Ensure no unconfined daemons exist
  echo
  echo \*\*\*\* Ensure\ no\ unconfined\ daemons\ exist
  echo Ensure\ no\ unconfined\ daemons\ exist Linux custom object not configured.

  # Ensure SELinux is installed
  echo
  echo \*\*\*\* Ensure\ SELinux\ is\ installed
  rpm -q libselinux || yum -y install libselinux

  # Ensure audit log storage size is configured
  echo
  echo \*\*\*\* Ensure\ audit\ log\ storage\ size\ is\ configured
  echo Ensure\ audit\ log\ storage\ size\ is\ configured not configured.

  # Ensure system is disabled when audit logs are full
  echo
  echo \*\*\*\* Ensure\ system\ is\ disabled\ when\ audit\ logs\ are\ full
  egrep -q "^(\s*)space_left_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)space_left_action\s*=\s*\S+(\s*#.*)?\s*$/\1space_left_action = email\2/" /etc/audit/auditd.conf || echo "space_left_action = email" >> /etc/audit/auditd.conf
  egrep -q "^(\s*)action_mail_acct\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)action_mail_acct\s*=\s*\S+(\s*#.*)?\s*$/\1action_mail_acct = root\2/" /etc/audit/auditd.conf || echo "action_mail_acct = root" >> /etc/audit/auditd.conf
  egrep -q "^(\s*)admin_space_left_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)admin_space_left_action\s*=\s*\S+(\s*#.*)?\s*$/\1admin_space_left_action = halt\2/" /etc/audit/auditd.conf || echo "admin_space_left_action = halt" >> /etc/audit/auditd.conf

  # Ensure audit logs are not automatically deleted
  echo
  echo \*\*\*\* Ensure\ audit\ logs\ are\ not\ automatically\ deleted
  egrep -q "^(\s*)max_log_file_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)max_log_file_action\s*=\s*\S+(\s*#.*)?\s*$/\1max_log_file_action = keep_logs\2/" /etc/audit/auditd.conf || echo "max_log_file_action = keep_logs" >> /etc/audit/auditd.conf

  # Ensure auditd service is enabled
  echo
  echo \*\*\*\* Ensure\ auditd\ service\ is\ enabled
  systemctl enable auditd.service

  # Ensure auditing for processes that start prior to auditd is enabled
  echo
  echo \*\*\*\* Ensure\ auditing\ for\ processes\ that\ start\ prior\ to\ auditd\ is\ enabled
  egrep -q "^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+)?\"(\s*#.*)?\s*$" /etc/default/grub && sed -ri '/^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]*)?\"(\s*#.*)?\s*$/ {/^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+\s+)?audit=\S+(\s+[^\"]+)?\"(\s*#.*)?\s*$/! s/^(\s*GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+)?)(\"(\s*#.*)?\s*)$/\1 audit=1\3/ }' /etc/default/grub && sed -ri "s/^((\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+\s+)?)audit=\S+((\s+[^\"]+)?\"(\s*#.*)?\s*)$/\1audit=1\4/" /etc/default/grub || echo "GRUB_CMDLINE_LINUX=\"audit=1\"" >> /etc/default/grub
  grub2-mkconfig -o /boot/grub2/grub.cfg

  # Ensure events that modify date and time information are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ date\ and\ time\ information\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+adjtimex\s+-S\s+settimeofday\s+-S\s+stime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+clock_settime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S clock_settime -k time-change" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/localtime\s+-p\s+wa\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/localtime -p wa -k time-change" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+adjtimex\s+-S\s+settimeofday\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+clock_settime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S clock_settime -k time-change" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify user/group information are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ user/group\ information\ are\ collected
  egrep "^-w\s+/etc/group\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/group -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/passwd\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/passwd -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/gshadow\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/gshadow -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/shadow\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/shadow -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/security/opasswd\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/security/opasswd -p wa -k identity" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify the system's network environment are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ the\ system\'s\ network\ environment\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+sethostname\s+-S\s+setdomainname\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/issue\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/issue -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/issue.net\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/issue.net -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/hosts\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/hosts -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/sysconfig/network\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sysconfig/network -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+sethostname\s+-S\s+setdomainname\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify the system's Mandatory Access Controls are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ the\ system\'s\ Mandatory\ Access\ Controls\ are\ collected
  egrep "^-w\s+/etc/selinux/\s+-p\s+wa\s+-k\s+MAC-policy\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/selinux/ -p wa -k MAC-policy" >> /etc/audit/rules.d/audit.rules

  # Ensure login and logout events are collected
  echo
  echo \*\*\*\* Ensure\ login\ and\ logout\ events\ are\ collected
  egrep "^-w\s+/var/run/faillock/\s+-p\s+wa\s+-k\s+logins\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/run/faillock/ -p wa -k logins" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/lastlog\s+-p\s+wa\s+-k\s+logins\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/lastlog -p wa -k logins" >> /etc/audit/rules.d/audit.rules

  # Ensure session initiation information is collected
  echo
  echo \*\*\*\* Ensure\ session\ initiation\ information\ is\ collected
  egrep "^-w\s+/var/run/utmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/run/utmp -p wa -k session" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/wtmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/wtmp -p wa -k session" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/btmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/btmp -p wa -k session" >> /etc/audit/rules.d/audit.rules

  # Ensure discretionary access control permission modification events are collected
  echo
  echo \*\*\*\* Ensure\ discretionary\ access\ control\ permission\ modification\ events\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+chmod\s+-S\s+fchmod\s+-S\s+fchmodat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+chown\s+-S\s+fchown\s+-S\s+fchownat\s+-S\s+lchown\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+setxattr\s+-S\s+lsetxattr\s+-S\s+fsetxattr\s+-S\s+removexattr\s+-S\s+lremovexattr\s+-S\s+fremovexattr\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+chmod\s+-S\s+fchmod\s+-S\s+fchmodat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+chown\s+-S\s+fchown\s+-S\s+fchownat\s+-S\s+lchown\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+setxattr\s+-S\s+lsetxattr\s+-S\s+fsetxattr\s+-S\s+removexattr\s+-S\s+lremovexattr\s+-S\s+fremovexattr\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules

  # Ensure unsuccessful unauthorized file access attempts are collected
  echo
  echo \*\*\*\* Ensure\ unsuccessful\ unauthorized\ file\ access\ attempts\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EACCES\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EPERM\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EACCES\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EPERM\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules

  # Ensure use of privileged commands is collected
  echo
  echo \*\*\*\* Ensure\ use\ of\ privileged\ commands\ is\ collected
  for file in `find / -xdev \( -perm -4000 -o -perm -2000 \) -type f`; do egrep -q "^\s*-a\s+(always,exit|exit,always)\s+-F\s+path=$file\s+-F\s+perm=x\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+privileged\s*(#.*)?$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F path=$file -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged" >> /etc/audit/rules.d/audit.rules; done

  # Ensure successful file system mounts are collected
  echo
  echo \*\*\*\* Ensure\ successful\ file\ system\ mounts\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+mount\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+mounts\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+mount\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+mounts\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts" >> /etc/audit/rules.d/audit.rules

  # Ensure file deletion events by users are collected
  echo
  echo \*\*\*\* Ensure\ file\ deletion\ events\ by\ users\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+unlink\s+-S\s+unlinkat\s+-S\s+rename\s+-S\s+renameat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+delete\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+unlink\s+-S\s+unlinkat\s+-S\s+rename\s+-S\s+renameat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+delete\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete" >> /etc/audit/rules.d/audit.rules

  # Ensure changes to system administration scope (sudoers) is collected
  echo
  echo \*\*\*\* Ensure\ changes\ to\ system\ administration\ scope\ \(sudoers\)\ is\ collected
  egrep "^-w\s+/etc/sudoers\s+-p\s+wa\s+-k\s+scope\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sudoers -p wa -k scope" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/sudoers.d\s+-p\s+wa\s+-k\s+scope\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sudoers.d -p wa -k scope" >> /etc/audit/rules.d/audit.rules

  # Ensure system administrator actions (sudolog) are collected
  echo
  echo \*\*\*\* Ensure\ system\ administrator\ actions\ \(sudolog\)\ are\ collected
  egrep "^-w\s+/var/log/sudo.log\s+-p\s+wa\s+-k\s+actions\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/sudo.log -p wa -k actions" >> /etc/audit/rules.d/audit.rules

  # Ensure kernel module loading and unloading is collected
  echo
  echo \*\*\*\* Ensure\ kernel\ module\ loading\ and\ unloading\ is\ collected
  egrep "^-w\s+/sbin/insmod\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/insmod -p x -k modules" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/sbin/rmmod\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/rmmod -p x -k modules" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/sbin/modprobe\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/modprobe -p x -k modules" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' || egrep "^-a\s+(always,exit|exit,always)\s+arch=b32\s+-S\s+init_module\s+-S\s+delete_module\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit arch=b32 -S init_module -S delete_module -k modules" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+arch=b64\s+-S\s+init_module\s+-S\s+delete_module\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit arch=b64 -S init_module -S delete_module -k modules" >> /etc/audit/rules.d/audit.rules

  # Ensure the audit configuration is immutable
  echo
  echo \*\*\*\* Ensure\ the\ audit\ configuration\ is\ immutable
  egrep "^-e\s+2\s*$" /etc/audit/rules.d/audit.rules || echo "-e 2" >> /etc/audit/rules.d/audit.rules
fi

if [ "$PROFILE" = "Level 1 - Workstation" ] || [ "$PROFILE" = "Level 2 - Workstation" ]; then
  echo \*\*\*\* Executing Level 1 - Workstation profile remediation

  # Ensure mounting of cramfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ cramfs\ filesystems\ is\ disabled
  modprobe -n -v cramfs | grep "^install /bin/true$" || echo "install cramfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^cramfs\s" && rmmod cramfs

  # Ensure mounting of freevxfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ freevxfs\ filesystems\ is\ disabled
  modprobe -n -v freevxfs | grep "^install /bin/true$" || echo "install freevxfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^freevxfs\s" && rmmod freevxfs

  # Ensure mounting of jffs2 filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ jffs2\ filesystems\ is\ disabled
  modprobe -n -v jffs2 | grep "^install /bin/true$" || echo "install jffs2 /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^jffs2\s" && rmmod jffs2

  # Ensure mounting of hfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ hfs\ filesystems\ is\ disabled
  modprobe -n -v hfs | grep "^install /bin/true$" || echo "install hfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^hfs\s" && rmmod hfs

  # Ensure mounting of hfsplus filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ hfsplus\ filesystems\ is\ disabled
  modprobe -n -v hfsplus | grep "^install /bin/true$" || echo "install hfsplus /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^hfsplus\s" && rmmod hfsplus

  # Ensure mounting of squashfs filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ squashfs\ filesystems\ is\ disabled
  modprobe -n -v squashfs | grep "^install /bin/true$" || echo "install squashfs /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^squashfs\s" && rmmod squashfs

  # Ensure mounting of udf filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ udf\ filesystems\ is\ disabled
  modprobe -n -v udf | grep "^install /bin/true$" || echo "install udf /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^udf\s" && rmmod udf

  # Ensure nodev option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /tmp\ partition
  echo Ensure\ nodev\ option\ set\ on\ /tmp\ partition not configured.

  # Ensure nosuid option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /tmp\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /tmp\ partition not configured.

  # Ensure noexec option set on /tmp partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /tmp\ partition
  echo Ensure\ noexec\ option\ set\ on\ /tmp\ partition not configured.

  # Ensure nodev option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ nodev\ option\ set\ on\ /var/tmp\ partition not configured.

  # Ensure nosuid option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /var/tmp\ partition not configured.

  # Ensure noexec option set on /var/tmp partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /var/tmp\ partition
  echo Ensure\ noexec\ option\ set\ on\ /var/tmp\ partition not configured.

  # Ensure nodev option set on /home partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /home\ partition
  echo Ensure\ nodev\ option\ set\ on\ /home\ partition not configured.

  # Ensure nodev option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ nodev\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ nodev\ option\ set\ on\ /dev/shm\ partition not configured.

  # Ensure nosuid option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ nosuid\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ nosuid\ option\ set\ on\ /dev/shm\ partition not configured.

  # Ensure noexec option set on /dev/shm partition
  echo
  echo \*\*\*\* Ensure\ noexec\ option\ set\ on\ /dev/shm\ partition
  echo Ensure\ noexec\ option\ set\ on\ /dev/shm\ partition not configured.

  # Ensure sticky bit is set on all world-writable directories
  echo
  echo \*\*\*\* Ensure\ sticky\ bit\ is\ set\ on\ all\ world-writable\ directories
  df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type d \( -perm -0002 -a ! -perm -1000 \) 2>/dev/null | xargs chmod a+t

  # Ensure gpgcheck is globally activated
  echo
  echo \*\*\*\* Ensure\ gpgcheck\ is\ globally\ activated
  egrep -q "^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$" /etc/yum.conf && sed -ri "s/^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$/\1gpgcheck=1\2/" /etc/yum.conf || echo "gpgcheck=1" >> /etc/yum.conf
  for file in /etc/yum.repos.d/*; do
    egrep -q "^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$" $file && sed -ri "s/^(\s*)gpgcheck\s*=\s*\S+(\s*#.*)?\s*$/\1gpgcheck=1\2/" $file || echo "gpgcheck=1" >> $file
  done

  # Ensure AIDE is installed
  echo
  echo \*\*\*\* Ensure\ AIDE\ is\ installed
  rpm -q aide || yum -y install aide

  # Ensure filesystem integrity is regularly checked
  echo
  echo \*\*\*\* Ensure\ filesystem\ integrity\ is\ regularly\ checked
  (crontab -u root -l; crontab -u root -l | egrep -q "^0 5 \* \* \* /usr/sbin/aide --check$" || echo "0 5 * * * /usr/sbin/aide --check" ) | crontab -u root -

  # Ensure permissions on bootloader config are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ bootloader\ config\ are\ configured
  chmod g-r-w-x,o-r-w-x /boot/grub2/grub.cfg

  # Ensure bootloader password is set
  echo
  echo \*\*\*\* Ensure\ bootloader\ password\ is\ set
  echo Ensure\ bootloader\ password\ is\ set not configured.

  # Ensure authentication required for single user mode
  echo
  echo \*\*\*\* Ensure\ authentication\ required\ for\ single\ user\ mode
  egrep -q "^\s*ExecStart" /usr/lib/systemd/system/rescue.service && sed -ri "s/(^[[:space:]]*ExecStart[[:space:]]*=[[:space:]]*).*$/\1-\/bin\/sh -c \"\/sbin\/sulogin; \/usr\/bin\/systemctl --fail --no-block default\"/" /usr/lib/systemd/system/rescue.service || echo "ExecStart=-/bin/sh -c \"/sbin/sulogin; /usr/bin/systemctl --fail --no-block default\"" >> /usr/lib/systemd/system/rescue.service
  egrep -q "^\s*ExecStart" /usr/lib/systemd/system/emergency.service && sed -ri "s/(^[[:space:]]*ExecStart[[:space:]]*=[[:space:]]*).*$/\1-\/bin\/sh -c \"\/sbin\/sulogin; \/usr\/bin\/systemctl --fail --no-block default\"/" /usr/lib/systemd/system/emergency.service || echo "ExecStart=-/bin/sh -c \"/sbin/sulogin; /usr/bin/systemctl --fail --no-block default\"" >> /usr/lib/systemd/system/emergency.service


  # Ensure core dumps are restricted
  echo
  echo \*\*\*\* Ensure\ core\ dumps\ are\ restricted
  egrep -q "^(\s*)\*\s+hard\s+core\s+\S+(\s*#.*)?\s*$" /etc/security/limits.conf && sed -ri "s/^(\s*)\*\s+hard\s+core\s+\S+(\s*#.*)?\s*$/\1* hard core 0\2/" /etc/security/limits.conf || echo "* hard core 0" >> /etc/security/limits.conf
  egrep -q "^(\s*)fs.suid_dumpable\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)fs.suid_dumpable\s*=\s*\S+(\s*#.*)?\s*$/\1fs.suid_dumpable = 0\2/" /etc/sysctl.conf || echo "fs.suid_dumpable = 0" >> /etc/sysctl.conf

  # Ensure XD/NX support is enabled
  echo
  echo \*\*\*\* Ensure\ XD/NX\ support\ is\ enabled
  echo Ensure\ XD/NX\ support\ is\ enabled not configured.

  # Ensure address space layout randomization (ASLR) is enabled
  echo
  echo \*\*\*\* Ensure\ address\ space\ layout\ randomization\ \(ASLR\)\ is\ enabled
  egrep -q "^(\s*)kernel.randomize_va_space\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)kernel.randomize_va_space\s*=\s*\S+(\s*#.*)?\s*$/\1kernel.randomize_va_space = 2\2/" /etc/sysctl.conf || echo "kernel.randomize_va_space = 2" >> /etc/sysctl.conf

  # Ensure prelink is disabled
  echo
  echo \*\*\*\* Ensure\ prelink\ is\ disabled
  rpm -q prelink && yum -y remove prelink

  # Ensure message of the day is configured properly
  echo
  echo \*\*\*\* Ensure\ message\ of\ the\ day\ is\ configured\ properly
  sed -ri 's/(\\v|\\r|\\m|\\s)//g' /etc/motd

  # Ensure local login warning banner is configured properly
  echo
  echo \*\*\*\* Ensure\ local\ login\ warning\ banner\ is\ configured\ properly
  echo "Authorized uses only. All activity may be monitored and reported." > /etc/issue

  # Ensure remote login warning banner is configured properly
  echo
  echo \*\*\*\* Ensure\ remote\ login\ warning\ banner\ is\ configured\ properly
  echo "Authorized uses only. All activity may be monitored and reported." > /etc/issue.net

  # Ensure permissions on /etc/motd are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/motd\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/motd

  # Ensure permissions on /etc/issue are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/issue\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/issue

  # Ensure permissions on /etc/issue.net are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/issue.net\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/issue.net

  # Ensure GDM login banner is configured
  echo
  echo \*\*\*\* Ensure\ GDM\ login\ banner\ is\ configured
  echo Ensure\ GDM\ login\ banner\ is\ configured not configured.

  # Ensure chargen services are not enabled
  echo
  echo \*\*\*\* Ensure\ chargen\ services\ are\ not\ enabled
  chkconfig chargen off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure daytime services are not enabled
  echo
  echo \*\*\*\* Ensure\ daytime\ services\ are\ not\ enabled
  chkconfig daytime off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure discard services are not enabled
  echo
  echo \*\*\*\* Ensure\ discard\ services\ are\ not\ enabled
  chkconfig discard off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure echo services are not enabled
  echo
  echo \*\*\*\* Ensure\ echo\ services\ are\ not\ enabled
  chkconfig echo off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure time services are not enabled
  echo
  echo \*\*\*\* Ensure\ time\ services\ are\ not\ enabled
  chkconfig time off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified

  # Ensure tftp server is not enabled
  echo
  echo \*\*\*\* Ensure\ tftp\ server\ is\ not\ enabled
  chkconfig tftp off
  echo /etc/inetd.conf and /etc/inetd.d/* unmodified
  systemctl disable tftp.socket.service

  # Ensure xinetd is not enabled
  echo
  echo \*\*\*\* Ensure\ xinetd\ is\ not\ enabled
  systemctl disable xinetd.service

  # Ensure time synchronization is in use
  echo
  echo \*\*\*\* Ensure\ time\ synchronization\ is\ in\ use
  rpm -q ntp || rpm -q chrony || yum -y install chrony

  # Ensure ntp is configured
  echo
  echo \*\*\*\* Ensure\ ntp\ is\ configured
  if rpm -q ntp >/dev/null; then
    egrep -q "^\s*restrict(\s+-4)?\s+default(\s+\S+)*(\s*#.*)?\s*$" /etc/ntp.conf && sed -ri "s/^(\s*)restrict(\s+-4)?\s+default(\s+[^[:space:]#]+)*(\s+#.*)?\s*$/\1restrict\2 default kod nomodify notrap nopeer noquery\4/" /etc/ntp.conf || echo "restrict default kod nomodify notrap nopeer noquery" >> /etc/ntp.conf 
    egrep -q "^\s*restrict\s+-6\s+default(\s+\S+)*(\s*#.*)?\s*$" /etc/ntp.conf && sed -ri "s/^(\s*)restrict\s+-6\s+default(\s+[^[:space:]#]+)*(\s+#.*)?\s*$/\1restrict -6 default kod nomodify notrap nopeer noquery\3/" /etc/ntp.conf || echo "restrict -6 default kod nomodify notrap nopeer noquery" >> /etc/ntp.conf 
    egrep -q "^(\s*)OPTIONS\s*=\s*\"(([^\"]+)?-u\s[^[:space:]\"]+([^\"]+)?|([^\"]+))\"(\s*#.*)?\s*$" /etc/sysconfig/ntpd && sed -ri '/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/ {/^(\s*)OPTIONS\s*=\s*\"[^\"]*-u\s+\S+[^\"]*\"(\s*#.*)?\s*$/! s/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/\1OPTIONS=\"\2 -u ntp:ntp\"\3/ }' /etc/sysconfig/ntpd && sed -ri "s/^(\s*)OPTIONS\s*=\s*\"([^\"]+\s+)?-u\s[^[:space:]\"]+(\s+[^\"]+)?\"(\s*#.*)?\s*$/\1OPTIONS=\"\2\-u ntp:ntp\3\"\4/" /etc/sysconfig/ntpd || echo "OPTIONS=\"-u ntp:ntp\"" >> /etc/sysconfig/ntpd
    echo Ensure ntp is configured - server not configured.
  fi

  # Ensure chrony is configured
  echo
  echo \*\*\*\* Ensure\ chrony\ is\ configured
  if rpm -q chrony >/dev/null; then
    egrep -q "^(\s*)OPTIONS\s*=\s*\"(([^\"]+)?-u\s[^[:space:]\"]+([^\"]+)?|([^\"]+))\"(\s*#.*)?\s*$" /etc/sysconfig/chronyd && sed -ri '/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/ {/^(\s*)OPTIONS\s*=\s*\"[^\"]*-u\s+\S+[^\"]*\"(\s*#.*)?\s*$/! s/^(\s*)OPTIONS\s*=\s*\"([^\"]*)\"(\s*#.*)?\s*$/\1OPTIONS=\"\2 -u chrony\"\3/ }' /etc/sysconfig/chronyd && sed -ri "s/^(\s*)OPTIONS\s*=\s*\"([^\"]+\s+)?-u\s[^[:space:]\"]+(\s+[^\"]+)?\"(\s*#.*)?\s*$/\1OPTIONS=\"\2\-u chrony\3\"\4/" /etc/sysconfig/chronyd || echo "OPTIONS=\"-u chrony\"" >> /etc/sysconfig/chronyd
    echo Ensure chrony is configured - server not configured.
  fi

  # Ensure Avahi Server is not enabled
  echo
  echo \*\*\*\* Ensure\ Avahi\ Server\ is\ not\ enabled
  systemctl disable avahi-daemon.service

  # Ensure DHCP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ DHCP\ Server\ is\ not\ enabled
  systemctl disable dhcpd.service

  # Ensure LDAP server is not enabled
  echo
  echo \*\*\*\* Ensure\ LDAP\ server\ is\ not\ enabled
  systemctl disable slapd.service

  # Ensure NFS and RPC are not enabled
  echo
  echo \*\*\*\* Ensure\ NFS\ and\ RPC\ are\ not\ enabled
  systemctl disable nfs.service
  systemctl disable rpcbind.service

  # Ensure DNS Server is not enabled
  echo
  echo \*\*\*\* Ensure\ DNS\ Server\ is\ not\ enabled
  systemctl disable named.service

  # Ensure FTP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ FTP\ Server\ is\ not\ enabled
  systemctl disable vsftpd.service

  # Ensure HTTP server is not enabled
  echo
  echo \*\*\*\* Ensure\ HTTP\ server\ is\ not\ enabled
  systemctl disable htttpd.service

  # Ensure IMAP and POP3 server is not enabled
  echo
  echo \*\*\*\* Ensure\ IMAP\ and\ POP3\ server\ is\ not\ enabled
  systemctl disable dovecot.service

  # Ensure Samba is not enabled
  echo
  echo \*\*\*\* Ensure\ Samba\ is\ not\ enabled
  systemctl disable smb.service

  # Ensure HTTP Proxy Server is not enabled
  echo
  echo \*\*\*\* Ensure\ HTTP\ Proxy\ Server\ is\ not\ enabled
  systemctl disable squid.service

  # Ensure SNMP Server is not enabled
  echo
  echo \*\*\*\* Ensure\ SNMP\ Server\ is\ not\ enabled
  systemctl disable snmpd.service

  # Ensure mail transfer agent is configured for local-only mode
  echo
  echo \*\*\*\* Ensure\ mail\ transfer\ agent\ is\ configured\ for\ local-only\ mode
  echo Ensure\ mail\ transfer\ agent\ is\ configured\ for\ local-only\ mode Linux custom object not configured.

  # Ensure NIS Server is not enabled
  echo
  echo \*\*\*\* Ensure\ NIS\ Server\ is\ not\ enabled
  systemctl disable ypserv.service

  # Ensure rsh server is not enabled
  echo
  echo \*\*\*\* Ensure\ rsh\ server\ is\ not\ enabled
  systemctl disable rsh.socket.service
  systemctl disable rlogin.socket.service
  systemctl disable rexec.socket.service

  # Ensure telnet server is not enabled
  echo
  echo \*\*\*\* Ensure\ telnet\ server\ is\ not\ enabled
  systemctl disable telnet.socket.service

  # Ensure rsync service is not enabled
  echo
  echo \*\*\*\* Ensure\ rsync\ service\ is\ not\ enabled
  systemctl disable rsyncd.service

  # Ensure talk server is not enabled
  echo
  echo \*\*\*\* Ensure\ talk\ server\ is\ not\ enabled
  systemctl disable ntalk.service

  # Ensure NIS Client is not installed
  echo
  echo \*\*\*\* Ensure\ NIS\ Client\ is\ not\ installed
  rpm -q ypbind && yum -y remove ypbind

  # Ensure rsh client is not installed
  echo
  echo \*\*\*\* Ensure\ rsh\ client\ is\ not\ installed
  rpm -q rsh && yum -y remove rsh

  # Ensure talk client is not installed
  echo
  echo \*\*\*\* Ensure\ talk\ client\ is\ not\ installed
  rpm -q talk && yum -y remove talk

  # Ensure telnet client is not installed
  echo
  echo \*\*\*\* Ensure\ telnet\ client\ is\ not\ installed
  rpm -q telnet && yum -y remove telnet

  # Ensure LDAP client is not installed
  echo
  echo \*\*\*\* Ensure\ LDAP\ client\ is\ not\ installed
  rpm -q openldap-clients && yum -y remove openldap-clients

  # Ensure IP forwarding is disabled
  echo
  echo \*\*\*\* Ensure\ IP\ forwarding\ is\ disabled
  egrep -q "^(\s*)net.ipv4.ip_forward\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.ip_forward\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.ip_forward = 0\2/" /etc/sysctl.conf || echo "net.ipv4.ip_forward = 0" >> /etc/sysctl.conf

  # Ensure packet redirect sending is disabled
  echo
  echo \*\*\*\* Ensure\ packet\ redirect\ sending\ is\ disabled
  egrep -q "^(\s*)net.ipv4.conf.all.send_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.send_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.send_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.send_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.send_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.send_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.send_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.send_redirects = 0" >> /etc/sysctl.conf

  # Ensure source routed packets are not accepted
  echo
  echo \*\*\*\* Ensure\ source\ routed\ packets\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_source_route = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_source_route = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.accept_source_route\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.accept_source_route = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.accept_source_route = 0" >> /etc/sysctl.conf

  # Ensure ICMP redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ ICMP\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.accept_redirects = 0" >> /etc/sysctl.conf

  # Ensure secure ICMP redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ secure\ ICMP\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv4.conf.all.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.secure_redirects = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.secure_redirects = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.secure_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.secure_redirects = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.secure_redirects = 1" >> /etc/sysctl.conf

  # Ensure suspicious packets are logged
  echo
  echo \*\*\*\* Ensure\ suspicious\ packets\ are\ logged
  egrep -q "^(\s*)net.ipv4.conf.all.log_martians\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.log_martians\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.log_martians = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.log_martians = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.log_martians\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.log_martians\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.log_martians = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.log_martians = 1" >> /etc/sysctl.conf

  # Ensure broadcast ICMP requests are ignored
  echo
  echo \*\*\*\* Ensure\ broadcast\ ICMP\ requests\ are\ ignored
  egrep -q "^(\s*)net.ipv4.icmp_echo_ignore_broadcasts\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.icmp_echo_ignore_broadcasts\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.icmp_echo_ignore_broadcasts = 1\2/" /etc/sysctl.conf || echo "net.ipv4.icmp_echo_ignore_broadcasts = 1" >> /etc/sysctl.conf

  # Ensure bogus ICMP responses are ignored
  echo
  echo \*\*\*\* Ensure\ bogus\ ICMP\ responses\ are\ ignored
  egrep -q "^(\s*)net.ipv4.icmp_ignore_bogus_error_responses\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.icmp_ignore_bogus_error_responses\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.icmp_ignore_bogus_error_responses = 1\2/" /etc/sysctl.conf || echo "net.ipv4.icmp_ignore_bogus_error_responses = 1" >> /etc/sysctl.conf

  # Ensure Reverse Path Filtering is enabled
  echo
  echo \*\*\*\* Ensure\ Reverse\ Path\ Filtering\ is\ enabled
  egrep -q "^(\s*)net.ipv4.conf.all.rp_filter\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.all.rp_filter\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.all.rp_filter = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.all.rp_filter = 1" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv4.conf.default.rp_filter\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.conf.default.rp_filter\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.conf.default.rp_filter = 1\2/" /etc/sysctl.conf || echo "net.ipv4.conf.default.rp_filter = 1" >> /etc/sysctl.conf

  # Ensure TCP SYN Cookies is enabled
  echo
  echo \*\*\*\* Ensure\ TCP\ SYN\ Cookies\ is\ enabled
  egrep -q "^(\s*)net.ipv4.tcp_syncookies\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv4.tcp_syncookies\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv4.tcp_syncookies = 1\2/" /etc/sysctl.conf || echo "net.ipv4.tcp_syncookies = 1" >> /etc/sysctl.conf

  # Ensure IPv6 router advertisements are not accepted
  echo
  echo \*\*\*\* Ensure\ IPv6\ router\ advertisements\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv6.conf.all.accept_ra\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.all.accept_ra\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.all.accept_ra = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.all.accept_ra = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv6.conf.default.accept_ra\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.default.accept_ra\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.default.accept_ra = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.default.accept_ra = 0" >> /etc/sysctl.conf

  # Ensure IPv6 redirects are not accepted
  echo
  echo \*\*\*\* Ensure\ IPv6\ redirects\ are\ not\ accepted
  egrep -q "^(\s*)net.ipv6.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.all.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.all.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.all.accept_redirects = 0" >> /etc/sysctl.conf
  egrep -q "^(\s*)net.ipv6.conf.default.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$" /etc/sysctl.conf && sed -ri "s/^(\s*)net.ipv6.conf.default.accept_redirects\s*=\s*\S+(\s*#.*)?\s*$/\1net.ipv6.conf.default.accept_redirects = 0\2/" /etc/sysctl.conf || echo "net.ipv6.conf.default.accept_redirects = 0" >> /etc/sysctl.conf

  # Ensure IPv6 is disabled
  echo
  echo \*\*\*\* Ensure\ IPv6\ is\ disabled
  echo Ensure\ IPv6\ is\ disabled not configured.

  # Ensure TCP Wrappers is installed
  echo
  echo \*\*\*\* Ensure\ TCP\ Wrappers\ is\ installed
  rpm -q tcp_wrappers || yum -y install tcp_wrappers
  rpm -q tcp_wrappers-libs || yum -y install tcp_wrappers-libs

  # Ensure /etc/hosts.allow is configured
  echo
  echo \*\*\*\* Ensure\ /etc/hosts.allow\ is\ configured
  touch /etc/hosts.allow

  # Ensure /etc/hosts.deny is configured
  echo
  echo \*\*\*\* Ensure\ /etc/hosts.deny\ is\ configured
  echo Ensure\ /etc/hosts.deny\ is\ configured not configured.

  # Ensure permissions on /etc/hosts.allow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/hosts.allow\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/hosts.allow

  # Ensure permissions on /etc/hosts.deny are 644
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/hosts.deny\ are\ 644
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/hosts.deny

  # Ensure DCCP is disabled
  echo
  echo \*\*\*\* Ensure\ DCCP\ is\ disabled
  modprobe -n -v dccp | grep "^install /bin/true$" || echo "install dccp /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^dccp\s" && rmmod dccp

  # Ensure SCTP is disabled
  echo
  echo \*\*\*\* Ensure\ SCTP\ is\ disabled
  modprobe -n -v sctp | grep "^install /bin/true$" || echo "install sctp /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^sctp\s" && rmmod sctp

  # Ensure RDS is disabled
  echo
  echo \*\*\*\* Ensure\ RDS\ is\ disabled
  modprobe -n -v rds | grep "^install /bin/true$" || echo "install rds /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^rds\s" && rmmod rds

  # Ensure TIPC is disabled
  echo
  echo \*\*\*\* Ensure\ TIPC\ is\ disabled
  modprobe -n -v tipc | grep "^install /bin/true$" || echo "install tipc /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^tipc\s" && rmmod tipc

  # Ensure iptables is installed
  echo
  echo \*\*\*\* Ensure\ iptables\ is\ installed
  rpm -q iptables || yum -y install iptables

  # Ensure default deny firewall policy
  echo
  echo \*\*\*\* Ensure\ default\ deny\ firewall\ policy
  echo Ensure\ default\ deny\ firewall\ policy not configured.

  # Ensure loopback traffic is configured
  echo
  echo \*\*\*\* Ensure\ loopback\ traffic\ is\ configured
  echo Ensure\ loopback\ traffic\ is\ configured not configured.

  # Ensure firewall rules exist for all open ports
  echo
  echo \*\*\*\* Ensure\ firewall\ rules\ exist\ for\ all\ open\ ports
  echo Ensure\ firewall\ rules\ exist\ for\ all\ open\ ports not configured.

  # Ensure rsyslog Service is enabled
  echo
  echo \*\*\*\* Ensure\ rsyslog\ Service\ is\ enabled
  rpm -q rsyslog && systemctl enable rsyslog.service

  # Ensure rsyslog default file permissions configured
  echo
  echo \*\*\*\* Ensure\ rsyslog\ default\ file\ permissions\ configured
  echo Ensure\ rsyslog\ default\ file\ permissions\ configured not configured.

  # Ensure rsyslog is configured to send logs to a remote log host
  echo
  echo \*\*\*\* Ensure\ rsyslog\ is\ configured\ to\ send\ logs\ to\ a\ remote\ log\ host
  echo Ensure\ rsyslog\ is\ configured\ to\ send\ logs\ to\ a\ remote\ log\ host not configured.

  # Ensure syslog-ng service is enabled
  echo
  echo \*\*\*\* Ensure\ syslog-ng\ service\ is\ enabled
  rpm -q syslog-ng && systemctl enable syslog-ng.service

  # Ensure syslog-ng default file permissions configured
  echo
  echo \*\*\*\* Ensure\ syslog-ng\ default\ file\ permissions\ configured
  echo Ensure\ syslog-ng\ default\ file\ permissions\ configured not configured.

  # Ensure rsyslog or syslog-ng is installed
  echo
  echo \*\*\*\* Ensure\ rsyslog\ or\ syslog-ng\ is\ installed
  rpm -q rsyslog || rpm -q syslog-ng || yum -y install rsyslog

  # Ensure permissions on all logfiles are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ all\ logfiles\ are\ configured
  chmod -R g-w-x,o-r-w-x /var/log/.*

  # Ensure cron daemon is enabled
  echo
  echo \*\*\*\* Ensure\ cron\ daemon\ is\ enabled
  systemctl enable crond.service

  # Ensure permissions on /etc/crontab are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/crontab\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/crontab

  # Ensure permissions on /etc/cron.hourly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.hourly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.hourly

  # Ensure permissions on /etc/cron.daily are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.daily\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.daily

  # Ensure permissions on /etc/cron.weekly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.weekly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.weekly

  # Ensure permissions on /etc/cron.monthly are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.monthly\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.monthly

  # Ensure permissions on /etc/cron.d are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/cron.d\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/cron.d

  # Ensure at/cron is restricted to authorized users
  echo
  echo \*\*\*\* Ensure\ at/cron\ is\ restricted\ to\ authorized\ users
  rm /etc/cron.deny
  rm /etc/at.deny
  chmod g-r-w-x,o-r-w-x /etc/cron.allow
  chmod g-r-w-x,o-r-w-x /etc/at.allow

  # Ensure permissions on /etc/ssh/sshd_config are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/ssh/sshd_config\ are\ configured
  chmod g-r-w-x,o-r-w-x /etc/ssh/sshd_config

  # Ensure SSH Protocol is set to 2
  echo
  echo \*\*\*\* Ensure\ SSH\ Protocol\ is\ set\ to\ 2
  egrep -q "^(\s*)Protocol\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Protocol\s+\S+(\s*#.*)?\s*$/\1Protocol 2\2/" /etc/ssh/sshd_config || echo "Protocol 2" >> /etc/ssh/sshd_config

  # Ensure SSH LogLevel is set to INFO
  echo
  echo \*\*\*\* Ensure\ SSH\ LogLevel\ is\ set\ to\ INFO
  egrep -q "^(\s*)LogLevel\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)LogLevel\s+\S+(\s*#.*)?\s*$/\1LogLevel INFO\2/" /etc/ssh/sshd_config || echo "LogLevel INFO" >> /etc/ssh/sshd_config

  # Ensure SSH X11 forwarding is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ X11\ forwarding\ is\ disabled
  egrep -q "^(\s*)X11Forwarding\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)X11Forwarding\s+\S+(\s*#.*)?\s*$/\1X11Forwarding no\2/" /etc/ssh/sshd_config || echo "X11Forwarding no" >> /etc/ssh/sshd_config

  # Ensure SSH MaxAuthTries is set to 4 or less
  echo
  echo \*\*\*\* Ensure\ SSH\ MaxAuthTries\ is\ set\ to\ 4\ or\ less
  egrep -q "^(\s*)MaxAuthTries\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)MaxAuthTries\s+\S+(\s*#.*)?\s*$/\1MaxAuthTries 4\2/" /etc/ssh/sshd_config || echo "MaxAuthTries 4" >> /etc/ssh/sshd_config

  # Ensure SSH IgnoreRhosts is enabled
  echo
  echo \*\*\*\* Ensure\ SSH\ IgnoreRhosts\ is\ enabled
  egrep -q "^(\s*)IgnoreRhosts\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)IgnoreRhosts\s+\S+(\s*#.*)?\s*$/\1IgnoreRhosts yes\2/" /etc/ssh/sshd_config || echo "IgnoreRhosts yes" >> /etc/ssh/sshd_config

  # Ensure SSH HostbasedAuthentication is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ HostbasedAuthentication\ is\ disabled
  egrep -q "^(\s*)HostbasedAuthentication\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)HostbasedAuthentication\s+\S+(\s*#.*)?\s*$/\1HostbasedAuthentication no\2/" /etc/ssh/sshd_config || echo "HostbasedAuthentication no" >> /etc/ssh/sshd_config

  # Ensure SSH root login is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ root\ login\ is\ disabled
  egrep -q "^(\s*)PermitRootLogin\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitRootLogin\s+\S+(\s*#.*)?\s*$/\1PermitRootLogin no\2/" /etc/ssh/sshd_config || echo "PermitRootLogin no" >> /etc/ssh/sshd_config

  # Ensure SSH PermitEmptyPasswords is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ PermitEmptyPasswords\ is\ disabled
  egrep -q "^(\s*)PermitEmptyPasswords\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitEmptyPasswords\s+\S+(\s*#.*)?\s*$/\1PermitEmptyPasswords no\2/" /etc/ssh/sshd_config || echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config

  # Ensure SSH PermitUserEnvironment is disabled
  echo
  echo \*\*\*\* Ensure\ SSH\ PermitUserEnvironment\ is\ disabled
  egrep -q "^(\s*)PermitUserEnvironment\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)PermitUserEnvironment\s+\S+(\s*#.*)?\s*$/\1PermitUserEnvironment no\2/" /etc/ssh/sshd_config || echo "PermitUserEnvironment no" >> /etc/ssh/sshd_config

  # Ensure only approved ciphers are used
  echo
  echo \*\*\*\* Ensure\ only\ approved\ ciphers\ are\ used
  egrep -q "^(\s*)Ciphers\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Ciphers\s+\S+(\s*#.*)?\s*$/\Ciphers aes256-ctr,aes192-ctr,aes128-ctr\2/" /etc/ssh/sshd_config || echo "Ciphers aes256-ctr,aes192-ctr,aes128-ctr" >> /etc/ssh/sshd_config

  # Ensure only approved MAC algorithms are used
  echo
  echo \*\*\*\* Ensure\ only\ approved\ MAC\ algorithms\ are\ used
  egrep -q "^(\s*)MACs\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)MACs\s+\S+(\s*#.*)?\s*$/\MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com\2/" /etc/ssh/sshd_config || echo "MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com" >> /etc/ssh/sshd_config

  # Ensure SSH Idle Timeout Interval is configured
  echo
  echo \*\*\*\* Ensure\ SSH\ Idle\ Timeout\ Interval\ is\ configured
  egrep -q "^(\s*)ClientAliveInterval\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)ClientAliveInterval\s+\S+(\s*#.*)?\s*$/\1ClientAliveInterval 300\2/" /etc/ssh/sshd_config || echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
  egrep -q "^(\s*)ClientAliveCountMax\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)ClientAliveCountMax\s+\S+(\s*#.*)?\s*$/\1ClientAliveCountMax 3\2/" /etc/ssh/sshd_config || echo "ClientAliveCountMax 3" >> /etc/ssh/sshd_config

  # Ensure SSH LoginGraceTime is set to one minute or less
  echo
  echo \*\*\*\* Ensure\ SSH\ LoginGraceTime\ is\ set\ to\ one\ minute\ or\ less
  egrep -q "^(\s*)LoginGraceTime\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)LoginGraceTime\s+\S+(\s*#.*)?\s*$/\1LoginGraceTime 60\2/" /etc/ssh/sshd_config || echo "LoginGraceTime 60" >> /etc/ssh/sshd_config

  # Ensure SSH access is limited
  echo
  echo \*\*\*\* Ensure\ SSH\ access\ is\ limited
  echo Ensure\ SSH\ access\ is\ limited not configured.

  # Ensure SSH warning banner is configured
  echo
  echo \*\*\*\* Ensure\ SSH\ warning\ banner\ is\ configured
  egrep -q "^(\s*)Banner\s+\S+(\s*#.*)?\s*$" /etc/ssh/sshd_config && sed -ri "s/^(\s*)Banner\s+\S+(\s*#.*)?\s*$/\1Banner \/etc\/issue.net\2/" /etc/ssh/sshd_config || echo "Banner /etc/issue.net" >> /etc/ssh/sshd_config

  # Ensure password creation requirements are configured
  echo
  echo \*\*\*\* Ensure\ password\ creation\ requirements\ are\ configured
  egrep -q "^(\s*)minlen\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)minlen\s*=\s*\S+(\s*#.*)?\s*$/\minlen=14\2/" /etc/security/pwquality.conf || echo "minlen=14" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)dcredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)dcredit\s*=\s*\S+(\s*#.*)?\s*$/\dcredit=-1\2/" /etc/security/pwquality.conf || echo "dcredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)ucredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)ucredit\s*=\s*\S+(\s*#.*)?\s*$/\ucredit=-1\2/" /etc/security/pwquality.conf || echo "ucredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)ocredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)ocredit\s*=\s*\S+(\s*#.*)?\s*$/\ocredit=-1\2/" /etc/security/pwquality.conf || echo "ocredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^(\s*)lcredit\s*=\s*\S+(\s*#.*)?\s*$" /etc/security/pwquality.conf && sed -ri "s/^(\s*)lcredit\s*=\s*\S+(\s*#.*)?\s*$/\lcredit=-1\2/" /etc/security/pwquality.conf || echo "lcredit=-1" >> /etc/security/pwquality.conf
  egrep -q "^\s*password\s+requisite\s+pam_pwquality.so\s+" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+try_first_pass)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1try_first_pass \2/ }' /etc/pam.d/system-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+retry=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1retry=3 \2/ }' /etc/pam.d/system-auth && sed -ri 's/(^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*\s+)retry=[0-9]+(\s+.*)?$/\1retry=3\3/' /etc/pam.d/system-auth || echo Ensure\ password\ creation\ requirements\ are\ configured - /etc/pam.d/system-auth not configured.
  egrep -q "^\s*password\s+requisite\s+pam_pwquality.so\s+" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+try_first_pass)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1try_first_pass \2/ }' /etc/pam.d/password-auth && sed -ri '/^\s*password\s+requisite\s+pam_pwquality.so\s+/ { /^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*(\s+retry=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+requisite\s+pam_pwquality.so\s+)(.*)$/\1retry=3 \2/ }' /etc/pam.d/password-auth && sed -ri 's/(^\s*password\s+requisite\s+pam_pwquality.so(\s+\S+)*\s+)retry=[0-9]+(\s+.*)?$/\1retry=3\3/' /etc/pam.d/password-auth || echo Ensure\ password\ creation\ requirements\ are\ configured - /etc/pam.d/password-auth not configured.

  # Ensure lockout for failed password attempts is configured
  echo
  echo \*\*\*\* Ensure\ lockout\ for\ failed\ password\ attempts\ is\ configured
  echo Ensure\ lockout\ for\ failed\ password\ attempts\ is\ configured not configured.

  # Ensure password reuse is limited
  echo
  echo \*\*\*\* Ensure\ password\ reuse\ is\ limited
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so(\s+.*)$" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+remember=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1remember=5 \2/ }' /etc/pam.d/system-auth && sed -ri 's/(^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*\s+)remember=[0-9]+(\s+.*)?$/\1remember=5\3/' /etc/pam.d/system-auth || echo Ensure\ password\ reuse\ is\ limited - /etc/pam.d/system-auth not configured.
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so(\s+.*)$" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+remember=[0-9]+)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1remember=5 \2/ }' /etc/pam.d/password-auth && sed -ri 's/(^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*\s+)remember=[0-9]+(\s+.*)?$/\1remember=5\3/' /etc/pam.d/password-auth || echo Ensure\ password\ reuse\ is\ limited - /etc/pam.d/password-auth not configured.

  # Ensure password hashing algorithm is SHA-512
  echo
  echo \*\*\*\* Ensure\ password\ hashing\ algorithm\ is\ SHA-512
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so\s+" /etc/pam.d/system-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+sha512)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1sha512 \2/ }' /etc/pam.d/system-auth || echo Ensure\ password\ hashing\ algorithm\ is\ SHA-512 - /etc/pam.d/password-auth not configured.
  egrep -q "^\s*password\s+sufficient\s+pam_unix.so\s+" /etc/pam.d/password-auth && sed -ri '/^\s*password\s+sufficient\s+pam_unix.so\s+/ { /^\s*password\s+sufficient\s+pam_unix.so(\s+\S+)*(\s+sha512)(\s+.*)?$/! s/^(\s*password\s+sufficient\s+pam_unix.so\s+)(.*)$/\1sha512 \2/ }' /etc/pam.d/password-auth || echo Ensure\ password\ hashing\ algorithm\ is\ SHA-512 - /etc/pam.d/password-auth not configured.

  # Ensure password expiration is 90 days or less
  echo
  echo \*\*\*\* Ensure\ password\ expiration\ is\ 90\ days\ or\ less
  egrep -q "^(\s*)PASS_MAX_DAYS\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_MAX_DAYS\s+\S+(\s*#.*)?\s*$/\PASS_MAX_DAYS 90\2/" /etc/login.defs || echo "PASS_MAX_DAYS 90" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --maxdays 90

  # Ensure minimum days between password changes is 7 or more
  echo
  echo \*\*\*\* Ensure\ minimum\ days\ between\ password\ changes\ is\ 7\ or\ more
  egrep -q "^(\s*)PASS_MIN_DAYS\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_MIN_DAYS\s+\S+(\s*#.*)?\s*$/\PASS_MIN_DAYS 7\2/" /etc/login.defs || echo "PASS_MIN_DAYS 7" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --mindays 7

  # Ensure password expiration warning days is 7 or more
  echo
  echo \*\*\*\* Ensure\ password\ expiration\ warning\ days\ is\ 7\ or\ more
  egrep -q "^(\s*)PASS_WARN_AGE\s+\S+(\s*#.*)?\s*$" /etc/login.defs && sed -ri "s/^(\s*)PASS_WARN_AGE\s+\S+(\s*#.*)?\s*$/\PASS_WARN_AGE 7\2/" /etc/login.defs || echo "PASS_WARN_AGE 7" >> /etc/login.defs
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --warndays 7

  # Ensure inactive password lock is 30 days or less
  echo
  echo \*\*\*\* Ensure\ inactive\ password\ lock\ is\ 30\ days\ or\ less
  useradd -D -f 30
  getent passwd | cut -f1 -d ":" | xargs -n1 chage --inactive 30

  # Ensure system accounts are non-login
  echo
  echo \*\*\*\* Ensure\ system\ accounts\ are\ non-login
  for user in `awk -F: '($3 < 1000) {print $1 }' /etc/passwd`; do
  if [ $user != "root" ]
  then
    /usr/sbin/usermod -L $user
    if [ $user != "sync" ] && [ $user != "shutdown" ] && [ $user != "halt" ]
    then
      /usr/sbin/usermod -s /sbin/nologin $user
    fi
  fi
done


  # Ensure default group for the root account is GID 0
  echo
  echo \*\*\*\* Ensure\ default\ group\ for\ the\ root\ account\ is\ GID\ 0
  usermod -g 0 root

  # Ensure default user umask is 027 or more restrictive
  echo
  echo \*\*\*\* Ensure\ default\ user\ umask\ is\ 027\ or\ more\ restrictive
  egrep -q "^(\s*)umask\s+\S+(\s*#.*)?\s*$" /etc/bashrc && sed -ri "s/^(\s*)umask\s+\S+(\s*#.*)?\s*$/\1umask 077\2/" /etc/bashrc || echo "umask 077" >> /etc/bashrc
  egrep -q "^(\s*)umask\s+\S+(\s*#.*)?\s*$" /etc/profile && sed -ri "s/^(\s*)umask\s+\S+(\s*#.*)?\s*$/\1umask 077\2/" /etc/profile || echo "umask 077" >> /etc/profile

  # Ensure access to the su command is restricted
  echo
  echo \*\*\*\* Ensure\ access\ to\ the\ su\ command\ is\ restricted
  egrep -q "^\s*auth\s+required\s+pam_wheel.so(\s+.*)?$" /etc/pam.d/su && sed -ri '/^\s*auth\s+required\s+pam_wheel.so(\s+.*)?$/ { /^\s*auth\s+required\s+pam_wheel.so(\s+\S+)*(\s+use_uid)(\s+.*)?$/! s/^(\s*auth\s+required\s+pam_wheel.so)(\s+.*)?$/\1 use_uid\2/ }' /etc/pam.d/su || echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su

  # Ensure permissions on /etc/passwd are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/passwd\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/passwd

  # Ensure permissions on /etc/shadow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/shadow\ are\ configured
  chmod -t,u-x-s,g-w-x-s,o-r-w-x /etc/shadow

  # Ensure permissions on /etc/group are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/group\ are\ configured
  chmod -t,u+r+w-x-s,g+r-w-x-s,o+r-w-x /etc/group

  # Ensure permissions on /etc/gshadow are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/gshadow\ are\ configured
  chmod -t,u-x-s,g-w-x-s,o-r-w-x /etc/gshadow

  # Ensure permissions on /etc/passwd- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/passwd-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/passwd-

  # Ensure permissions on /etc/shadow- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/shadow-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/shadow-

  # Ensure permissions on /etc/group- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/group-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/group-

  # Ensure permissions on /etc/gshadow- are configured
  echo
  echo \*\*\*\* Ensure\ permissions\ on\ /etc/gshadow-\ are\ configured
  chmod -t,u-x-s,g-r-w-x-s,o-r-w-x /etc/gshadow-

  # Ensure no world writable files exist
  echo
  echo \*\*\*\* Ensure\ no\ world\ writable\ files\ exist
  echo Ensure\ no\ world\ writable\ files\ exist Linux custom object not configured.

  # Ensure no unowned files or directories exist
  echo
  echo \*\*\*\* Ensure\ no\ unowned\ files\ or\ directories\ exist
  echo Ensure\ no\ unowned\ files\ or\ directories\ exist Linux custom object not configured.

  # Ensure no ungrouped files or directories exist
  echo
  echo \*\*\*\* Ensure\ no\ ungrouped\ files\ or\ directories\ exist
  echo Ensure\ no\ ungrouped\ files\ or\ directories\ exist Linux custom object not configured.

  # Ensure password fields are not empty
  echo
  echo \*\*\*\* Ensure\ password\ fields\ are\ not\ empty
  echo Ensure\ password\ fields\ are\ not\ empty not configured.

  # Ensure no legacy &quot;+&quot; entries exist in /etc/passwd
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/passwd
  sed -ri '/^\+:.*$/ d' /etc/passwd

  # Ensure no legacy &quot;+&quot; entries exist in /etc/shadow
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/shadow
  sed -ri '/^\+:.*$/ d' /etc/shadow

  # Ensure no legacy &quot;+&quot; entries exist in /etc/group
  echo
  echo \*\*\*\* Ensure\ no\ legacy\ \&quot\;\+\&quot\;\ entries\ exist\ in\ /etc/group
  sed -ri '/^\+:.*$/ d' /etc/group

  # Ensure root is the only UID 0 account
  echo
  echo \*\*\*\* Ensure\ root\ is\ the\ only\ UID\ 0\ account
  echo Ensure\ root\ is\ the\ only\ UID\ 0\ account not configured.

  # Ensure root PATH Integrity
  echo
  echo \*\*\*\* Ensure\ root\ PATH\ Integrity
  echo Ensure\ root\ PATH\ Integrity Linux custom object not configured.

  # Ensure all users' home directories exist
  echo
  echo \*\*\*\* Ensure\ all\ users\'\ home\ directories\ exist
  echo Ensure\ all\ users\'\ home\ directories\ exist Linux custom object not configured.

  # Ensure users' home directories permissions are 750 or more restrictive
  echo
  echo \*\*\*\* Ensure\ users\'\ home\ directories\ permissions\ are\ 750\ or\ more\ restrictive
  echo Ensure\ users\'\ home\ directories\ permissions\ are\ 750\ or\ more\ restrictive Linux custom object not configured.

  # Ensure users own their home directories
  echo
  echo \*\*\*\* Ensure\ users\ own\ their\ home\ directories
  echo Ensure\ users\ own\ their\ home\ directories not configured.

  # Ensure users' dot files are not group or world writable
  echo
  echo \*\*\*\* Ensure\ users\'\ dot\ files\ are\ not\ group\ or\ world\ writable
  echo Ensure\ users\'\ dot\ files\ are\ not\ group\ or\ world\ writable Linux custom object not configured.

  # Ensure no users have .forward files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .forward\ files
  echo Ensure\ no\ users\ have\ .forward\ files Linux custom object not configured.

  # Ensure no users have .netrc files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .netrc\ files
  echo Ensure\ no\ users\ have\ .netrc\ files Linux custom object not configured.

  # Ensure users' .netrc Files are not group or world accessible
  echo
  echo \*\*\*\* Ensure\ users\'\ .netrc\ Files\ are\ not\ group\ or\ world\ accessible
  echo Ensure\ users\'\ .netrc\ Files\ are\ not\ group\ or\ world\ accessible Linux custom object not configured.

  # Ensure no users have .rhosts files
  echo
  echo \*\*\*\* Ensure\ no\ users\ have\ .rhosts\ files
  echo Ensure\ no\ users\ have\ .rhosts\ files Linux custom object not configured.

  # Ensure all groups in /etc/passwd exist in /etc/group
  echo
  echo \*\*\*\* Ensure\ all\ groups\ in\ /etc/passwd\ exist\ in\ /etc/group
  echo Ensure\ all\ groups\ in\ /etc/passwd\ exist\ in\ /etc/group Linux custom object not configured.

  # Ensure no duplicate UIDs exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ UIDs\ exist
  echo Ensure\ no\ duplicate\ UIDs\ exist Linux custom object not configured.

  # Ensure no duplicate GIDs exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ GIDs\ exist
  echo Ensure\ no\ duplicate\ GIDs\ exist Linux custom object not configured.

  # Ensure no duplicate user names exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ user\ names\ exist
  echo Ensure\ no\ duplicate\ user\ names\ exist Linux custom object not configured.

  # Ensure no duplicate group names exist
  echo
  echo \*\*\*\* Ensure\ no\ duplicate\ group\ names\ exist
  echo Ensure\ no\ duplicate\ group\ names\ exist Linux custom object not configured.
fi

if [ "$PROFILE" = "Level 2 - Workstation" ]; then
  echo \*\*\*\* Executing Level 2 - Workstation profile remediation

  # Ensure mounting of FAT filesystems is disabled
  echo
  echo \*\*\*\* Ensure\ mounting\ of\ FAT\ filesystems\ is\ disabled
  modprobe -n -v vfat | grep "^install /bin/true$" || echo "install vfat /bin/true" >> /etc/modprobe.d/CIS.conf
  lsmod | egrep "^vfat\s" && rmmod vfat

  # Ensure separate partition exists for /tmp
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /tmp
  echo Ensure\ separate\ partition\ exists\ for\ /tmp not configured.

  # Ensure separate partition exists for /var
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var
  echo Ensure\ separate\ partition\ exists\ for\ /var not configured.

  # Ensure separate partition exists for /var/tmp
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/tmp
  echo Ensure\ separate\ partition\ exists\ for\ /var/tmp not configured.

  # Ensure separate partition exists for /var/log
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/log
  echo Ensure\ separate\ partition\ exists\ for\ /var/log not configured.

  # Ensure separate partition exists for /var/log/audit
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /var/log/audit
  echo Ensure\ separate\ partition\ exists\ for\ /var/log/audit not configured.

  # Ensure separate partition exists for /home
  echo
  echo \*\*\*\* Ensure\ separate\ partition\ exists\ for\ /home
  echo Ensure\ separate\ partition\ exists\ for\ /home not configured.

  # Disable Automounting
  echo
  echo \*\*\*\* Disable\ Automounting
  systemctl disable autofs.service

  # Ensure SELinux is not disabled in bootloader configuration
  echo
  echo \*\*\*\* Ensure\ SELinux\ is\ not\ disabled\ in\ bootloader\ configuration
  echo Ensure\ SELinux\ is\ not\ disabled\ in\ bootloader\ configuration not configured.

  # Ensure the SELinux state is enforcing
  echo
  echo \*\*\*\* Ensure\ the\ SELinux\ state\ is\ enforcing
  echo Ensure\ the\ SELinux\ state\ is\ enforcing not configured.

  # Ensure SELinux policy is configured
  echo
  echo \*\*\*\* Ensure\ SELinux\ policy\ is\ configured
  echo Ensure\ SELinux\ policy\ is\ configured not configured.

  # Ensure the MCS Translation Service (mcstrans) is not installed
  echo
  echo \*\*\*\* Ensure\ the\ MCS\ Translation\ Service\ \(mcstrans\)\ is\ not\ installed
  rpm -q mcstrans && yum -y remove mcstrans

  # Ensure no unconfined daemons exist
  echo
  echo \*\*\*\* Ensure\ no\ unconfined\ daemons\ exist
  echo Ensure\ no\ unconfined\ daemons\ exist Linux custom object not configured.

  # Ensure SELinux is installed
  echo
  echo \*\*\*\* Ensure\ SELinux\ is\ installed
  rpm -q libselinux || yum -y install libselinux

  # Ensure CUPS is not enabled
  echo
  echo \*\*\*\* Ensure\ CUPS\ is\ not\ enabled
  systemctl disable cups.service

  # Ensure audit log storage size is configured
  echo
  echo \*\*\*\* Ensure\ audit\ log\ storage\ size\ is\ configured
  echo Ensure\ audit\ log\ storage\ size\ is\ configured not configured.

  # Ensure system is disabled when audit logs are full
  echo
  echo \*\*\*\* Ensure\ system\ is\ disabled\ when\ audit\ logs\ are\ full
  egrep -q "^(\s*)space_left_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)space_left_action\s*=\s*\S+(\s*#.*)?\s*$/\1space_left_action = email\2/" /etc/audit/auditd.conf || echo "space_left_action = email" >> /etc/audit/auditd.conf
  egrep -q "^(\s*)action_mail_acct\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)action_mail_acct\s*=\s*\S+(\s*#.*)?\s*$/\1action_mail_acct = root\2/" /etc/audit/auditd.conf || echo "action_mail_acct = root" >> /etc/audit/auditd.conf
  egrep -q "^(\s*)admin_space_left_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)admin_space_left_action\s*=\s*\S+(\s*#.*)?\s*$/\1admin_space_left_action = halt\2/" /etc/audit/auditd.conf || echo "admin_space_left_action = halt" >> /etc/audit/auditd.conf

  # Ensure audit logs are not automatically deleted
  echo
  echo \*\*\*\* Ensure\ audit\ logs\ are\ not\ automatically\ deleted
  egrep -q "^(\s*)max_log_file_action\s*=\s*\S+(\s*#.*)?\s*$" /etc/audit/auditd.conf && sed -ri "s/^(\s*)max_log_file_action\s*=\s*\S+(\s*#.*)?\s*$/\1max_log_file_action = keep_logs\2/" /etc/audit/auditd.conf || echo "max_log_file_action = keep_logs" >> /etc/audit/auditd.conf

  # Ensure auditd service is enabled
  echo
  echo \*\*\*\* Ensure\ auditd\ service\ is\ enabled
  systemctl enable auditd.service

  # Ensure auditing for processes that start prior to auditd is enabled
  echo
  echo \*\*\*\* Ensure\ auditing\ for\ processes\ that\ start\ prior\ to\ auditd\ is\ enabled
  egrep -q "^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+)?\"(\s*#.*)?\s*$" /etc/default/grub && sed -ri '/^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]*)?\"(\s*#.*)?\s*$/ {/^(\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+\s+)?audit=\S+(\s+[^\"]+)?\"(\s*#.*)?\s*$/! s/^(\s*GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+)?)(\"(\s*#.*)?\s*)$/\1 audit=1\3/ }' /etc/default/grub && sed -ri "s/^((\s*)GRUB_CMDLINE_LINUX\s*=\s*\"([^\"]+\s+)?)audit=\S+((\s+[^\"]+)?\"(\s*#.*)?\s*)$/\1audit=1\4/" /etc/default/grub || echo "GRUB_CMDLINE_LINUX=\"audit=1\"" >> /etc/default/grub
  grub2-mkconfig -o /boot/grub2/grub.cfg

  # Ensure events that modify date and time information are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ date\ and\ time\ information\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+adjtimex\s+-S\s+settimeofday\s+-S\s+stime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+clock_settime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S clock_settime -k time-change" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/localtime\s+-p\s+wa\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/localtime -p wa -k time-change" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+adjtimex\s+-S\s+settimeofday\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+clock_settime\s+-k\s+time-change\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S clock_settime -k time-change" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify user/group information are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ user/group\ information\ are\ collected
  egrep "^-w\s+/etc/group\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/group -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/passwd\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/passwd -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/gshadow\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/gshadow -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/shadow\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/shadow -p wa -k identity" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/security/opasswd\s+-p\s+wa\s+-k\s+identity\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/security/opasswd -p wa -k identity" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify the system's network environment are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ the\ system\'s\ network\ environment\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+sethostname\s+-S\s+setdomainname\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/issue\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/issue -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/issue.net\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/issue.net -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/hosts\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/hosts -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/sysconfig/network\s+-p\s+wa\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sysconfig/network -p wa -k system-locale" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+sethostname\s+-S\s+setdomainname\s+-k\s+system-locale\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale" >> /etc/audit/rules.d/audit.rules

  # Ensure events that modify the system's Mandatory Access Controls are collected
  echo
  echo \*\*\*\* Ensure\ events\ that\ modify\ the\ system\'s\ Mandatory\ Access\ Controls\ are\ collected
  egrep "^-w\s+/etc/selinux/\s+-p\s+wa\s+-k\s+MAC-policy\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/selinux/ -p wa -k MAC-policy" >> /etc/audit/rules.d/audit.rules

  # Ensure login and logout events are collected
  echo
  echo \*\*\*\* Ensure\ login\ and\ logout\ events\ are\ collected
  egrep "^-w\s+/var/run/faillock/\s+-p\s+wa\s+-k\s+logins\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/run/faillock/ -p wa -k logins" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/lastlog\s+-p\s+wa\s+-k\s+logins\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/lastlog -p wa -k logins" >> /etc/audit/rules.d/audit.rules

  # Ensure session initiation information is collected
  echo
  echo \*\*\*\* Ensure\ session\ initiation\ information\ is\ collected
  egrep "^-w\s+/var/run/utmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/run/utmp -p wa -k session" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/wtmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/wtmp -p wa -k session" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/var/log/btmp\s+-p\s+wa\s+-k\s+session\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/btmp -p wa -k session" >> /etc/audit/rules.d/audit.rules

  # Ensure discretionary access control permission modification events are collected
  echo
  echo \*\*\*\* Ensure\ discretionary\ access\ control\ permission\ modification\ events\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+chmod\s+-S\s+fchmod\s+-S\s+fchmodat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+chown\s+-S\s+fchown\s+-S\s+fchownat\s+-S\s+lchown\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+setxattr\s+-S\s+lsetxattr\s+-S\s+fsetxattr\s+-S\s+removexattr\s+-S\s+lremovexattr\s+-S\s+fremovexattr\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+chmod\s+-S\s+fchmod\s+-S\s+fchmodat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+chown\s+-S\s+fchown\s+-S\s+fchownat\s+-S\s+lchown\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+setxattr\s+-S\s+lsetxattr\s+-S\s+fsetxattr\s+-S\s+removexattr\s+-S\s+lremovexattr\s+-S\s+fremovexattr\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+perm_mod\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod" >> /etc/audit/rules.d/audit.rules

  # Ensure unsuccessful unauthorized file access attempts are collected
  echo
  echo \*\*\*\* Ensure\ unsuccessful\ unauthorized\ file\ access\ attempts\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EACCES\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EPERM\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EACCES\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+creat\s+-S\s+open\s+-S\s+openat\s+-S\s+truncate\s+-S\s+ftruncate\s+-F\s+exit=-EPERM\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+access\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EPERM -F auid>=1000 -F auid!=4294967295 -k access" >> /etc/audit/rules.d/audit.rules

  # Ensure use of privileged commands is collected
  echo
  echo \*\*\*\* Ensure\ use\ of\ privileged\ commands\ is\ collected
  for file in `find / -xdev \( -perm -4000 -o -perm -2000 \) -type f`; do egrep -q "^\s*-a\s+(always,exit|exit,always)\s+-F\s+path=$file\s+-F\s+perm=x\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+privileged\s*(#.*)?$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F path=$file -F perm=x -F auid>=1000 -F auid!=4294967295 -k privileged" >> /etc/audit/rules.d/audit.rules; done

  # Ensure successful file system mounts are collected
  echo
  echo \*\*\*\* Ensure\ successful\ file\ system\ mounts\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+mount\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+mounts\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+mount\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+mounts\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S mount -F auid>=1000 -F auid!=4294967295 -k mounts" >> /etc/audit/rules.d/audit.rules

  # Ensure file deletion events by users are collected
  echo
  echo \*\*\*\* Ensure\ file\ deletion\ events\ by\ users\ are\ collected
  egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b32\s+-S\s+unlink\s+-S\s+unlinkat\s+-S\s+rename\s+-S\s+renameat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+delete\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+-F\s+arch=b64\s+-S\s+unlink\s+-S\s+unlinkat\s+-S\s+rename\s+-S\s+renameat\s+-F\s+auid>=1000\s+-F\s+auid!=4294967295\s+-k\s+delete\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete" >> /etc/audit/rules.d/audit.rules

  # Ensure changes to system administration scope (sudoers) is collected
  echo
  echo \*\*\*\* Ensure\ changes\ to\ system\ administration\ scope\ \(sudoers\)\ is\ collected
  egrep "^-w\s+/etc/sudoers\s+-p\s+wa\s+-k\s+scope\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sudoers -p wa -k scope" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/etc/sudoers.d\s+-p\s+wa\s+-k\s+scope\s*$" /etc/audit/rules.d/audit.rules || echo "-w /etc/sudoers.d -p wa -k scope" >> /etc/audit/rules.d/audit.rules

  # Ensure system administrator actions (sudolog) are collected
  echo
  echo \*\*\*\* Ensure\ system\ administrator\ actions\ \(sudolog\)\ are\ collected
  egrep "^-w\s+/var/log/sudo.log\s+-p\s+wa\s+-k\s+actions\s*$" /etc/audit/rules.d/audit.rules || echo "-w /var/log/sudo.log -p wa -k actions" >> /etc/audit/rules.d/audit.rules

  # Ensure kernel module loading and unloading is collected
  echo
  echo \*\*\*\* Ensure\ kernel\ module\ loading\ and\ unloading\ is\ collected
  egrep "^-w\s+/sbin/insmod\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/insmod -p x -k modules" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/sbin/rmmod\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/rmmod -p x -k modules" >> /etc/audit/rules.d/audit.rules
  egrep "^-w\s+/sbin/modprobe\s+-p\s+x\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-w /sbin/modprobe -p x -k modules" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' || egrep "^-a\s+(always,exit|exit,always)\s+arch=b32\s+-S\s+init_module\s+-S\s+delete_module\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit arch=b32 -S init_module -S delete_module -k modules" >> /etc/audit/rules.d/audit.rules
  uname -p | grep -q 'x86_64' && egrep "^-a\s+(always,exit|exit,always)\s+arch=b64\s+-S\s+init_module\s+-S\s+delete_module\s+-k\s+modules\s*$" /etc/audit/rules.d/audit.rules || echo "-a always,exit arch=b64 -S init_module -S delete_module -k modules" >> /etc/audit/rules.d/audit.rules

  # Ensure the audit configuration is immutable
  echo
  echo \*\*\*\* Ensure\ the\ audit\ configuration\ is\ immutable
  egrep "^-e\s+2\s*$" /etc/audit/rules.d/audit.rules || echo "-e 2" >> /etc/audit/rules.d/audit.rules
fi
```
