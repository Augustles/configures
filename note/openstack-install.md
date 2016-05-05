# openstack devstack&&Mirantis Fuel
#####http://fosskb.in/2015/04/18/installing-openstack-kilo-on-ubuntu-15-04-single-machine-setup/
#####http://openstack-cloud-mylearning.blogspot.com/2015/02/openstack-juno-devstack-installation.html
#####http://www.chenshake.com/install-ubuntu-14-04-devstack/
#####http://chianingwang.blogspot.com/2014/11/how-to-install-openstack-juno-on.html
#####http://samuraiincloud.com/2014/08/13/building-openstack-icehouse-in-virtualbox-in-60-minutes-using-mirantis-fuel-2/
####配置网络
    sudo apt-get install bridge-utils
####安装配置ntp
    sudo apt-get install ntp
####安装mysql
    sudo apt-get install mysql-server python-mysqldb
####keystone验证
    apt-get install -y keystone
    mysql -u root -p
    CREATE DATABASE keystone;
    GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'keystone_dbpass';
#####/etc/keystone/keystone.conf
    connection = mysql://keystone:keystone_dbpass@0.0.0.0/keystone
    service keystone restart
    keystone-manage db_sync
    ketystone user-list
####安装glances
    sudo apt-get install glance
    glance image-list
####安装nova
    sudo apt-get install rabbitmq-server nova-common nova-doc python-nova nova-api nova-network nova-volume nova-objectstore nova-scheduler nova-compute
    sudo apt-get install -y euca2ools
    sudo apt-get install -y unzip
    nova list


