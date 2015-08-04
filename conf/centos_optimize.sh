#!/bin/bash
#该脚本用于关闭服务器上非必须的系统服务项，并不适用于所有服务器，比如如果是文件服务器则NFS相关服务则不能关闭
#定义所要停止的服务，可以根据实际服务器应用更改
SERVICES="acpid atd auditd avahi-daemon bluetooth cups firstboot hidd ip6tables kudzu lvm2-monitor mcstrans mdmonitor microcode_ctl netfs nfslock pcscd portmap rpcgssd rpcidmapd xfs yum-updatesd"
for service in $SERVICES
do
#关闭服务随系统启动
chkconfig $service off
#停止选择服务
service $service stop
done

#删除无用的用户和组,rsync
users = "adm lp shutdown halt uucp operator games gopher"
for user in $users
do
    #删除无用用户
    userdel $user
done
groups = "adm lp dip"
for group in $groups
do
    #删除无用组
    groupdel $group
done
#添加不可更改属性,需要修改chattr -i
chattr +i /etc/passwd
chattr +i /etc/shadow
chattr +i /etc/group
chattr +i /etc/gshadow

cpuver=`uname -i`
osver=`cat /etc/redhat-release |awk '{print substr($3,1,1)}'`

cat << EOF
start optimizing.......
EOF

#set DNS
cat > /etc/resolv.conf << EOF
nameserver 114.114.114.114
nameserver 8.8.8.8
EOF

#add the third-party repo and change timezone
yum -y install wget
wget -q -O - http://www.atomicorp.com/installers/atomic | sh
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#update the system and set the ntp
yum clean all
yum -y update glibc\*
yum -y update yum\* rpm\* python\* 
yum -y update
yum -y install ntp setuptool ntsysv system-config-network-tui openssh-clients
echo "* 4 * * * /usr/sbin/ntpdate 210.72.145.44 > /dev/null 2>&1" >> /etc/crontab
/etc/init.d/crond restart

#set the file limit
echo "ulimit -SHn 102400" >> /etc/rc.local 
cat >> /etc/security/limits.conf << EOF
*           soft   nofile       65535
*           hard   nofile       65535
EOF

#set the control-alt-delete
if [ $osver = "5" ]; then
sed -i 's/ca::ctrlaltdel/#ca::ctrlaltdel/g' /etc/inittab
else
sed -i 's#exec /sbin/shutdown -r now#\#exec /sbin/shutdown -r now#g' /etc/init/control-alt-delete.conf
fi

#disable selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
setenforce 0

#set ssh
#sed -i 's/#Port 22/Port 1015/g' /etc/ssh/sshd_config
sed -i 's/^GSSAPIAuthentication yes$/GSSAPIAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
/etc/init.d/sshd restart

#set kernel
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_syn_retries = 1
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.netdev_max_backlog = 262144
net.core.somaxconn = 262144
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 262144
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
EOF
/sbin/sysctl -p

#Disable IPV6 -- need reboot os
if [ $osver = "5" ]; then
cat >> /etc/modprobe.conf << EOF
install ipv6 /bin/true
EOF
else
cat > /etc/modprobe.d/ipv6.conf << EOF
install ipv6 /bin/true
EOF
fi
sed -i 's/^NETWORKING_IPV6=yes/NETWORKING_IPV6=no/g' /etc/sysconfig/network
echo "IPV6INIT=no" >> /etc/sysconfig/network

#Stop some server
chkconfig apmd off
chkconfig autofs off
chkconfig bluetooth off
chkconfig cups off
chkconfig ip6tables off
chkconfig iptables off
chkconfig hidd off
chkconfig idsn off 
chkconfig pcscd off
chkconfig pcmcia off
chkconfig sendmail off
chkconfig yum-updatesd off

cat << EOF
+-------------------------------------------------+
|               optimizer is done                 |
|           please reboot this server !           |
+-------------------------------------------------+
EOF
