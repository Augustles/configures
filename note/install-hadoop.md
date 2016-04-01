# hadoop

####ssh
* sudo useradd -m hadoop -s /bin/bash
* sudo passwd hadoop
* sudo adduser hadoop sudo
* sudo apt-get update
* sudo apt-get install openssh-server
* cd ~/.ssh/
* ssh-keygen -t rsa
* cat ./id_rsa.pub >> ./authorized_keys; # 免密码登录
####install java
* sudo apt-get install openjdk-7-jre openjdk-7-jdk
* dpkg -L openjdk-7-jdk | grep '/bin/javac'; # 检查路径
* export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/bin/javac
* java -version
