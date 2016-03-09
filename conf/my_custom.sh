# root ubuntu14.04 scrapy
sudo apt-get update
sudo apt-get -y install zsh vim git python python-pip wget curl
sudo apt-get -y install python-dev
sudo apt-get install -y libevent-dev libxml2-dev libxslt1-dev
sudo apt-get install -y libssl-dev libcurl4-openssl-dev python-dev
sudo apt-get install -y build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3
sudo pip install scrapy
sudo pip install pyOpenSSL==0.13
sudo pip install beautisoupful4
# check scrapy
scrapy -h
# mongo
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
#check mongo 进程
ps -aux | grep mongo
# 检查mongo端口
# netstat -nlt | grep 27017
