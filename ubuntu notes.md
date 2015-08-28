# ubuntu/centos笔记
#### 软件源优化
#### 常用软件
	sudo apt-get install zsh vim git python python-pip wget curl
	sudo apt-get install python-dev libffi-dev libxml2-dev libxslt1-dev libssl-dev libmysqlclient-dev
	sudo apt-get install ranger htop dstat glances screen slurm
	sudo pip install virtualenv virtualenvwrapper
	which virtualenvwrapper
	pip install ipython glances cheat fabric ipdb sh
	
	sudo yum install python-devel libxml2-devel python-setuptools zlib-devel wget pcre-devel gcc make mysql-devel
#### deb,rpm软件安装
	dpkg -i file.deb
	rpm -ivh file.rpm
#### 安装字体Monaco
	curl -kL https://raw.github.com/cstrap/monaco-font/master/install-font-ubuntu.sh | bash   sudo apt-get install ttf-wqy-zenhei
#### 安装输入法
	sudo apt-get install ibus ibus-pinyin
	ibus-daemon -d -x -r
#### 安装主题
	sudo apt-get install unity-tweak-tool
#### 安装新立得(软件管理)
	sudo apt-get install synaptic
#### 安装程序启动器
	sudo add-apt-repository ppa:synapse-core/ppa
	sudo apt-get install Synapse
#### 安装flash
	sudo apt-get install flashplugin-instaler
#### 安装压缩解压增强
	sudo apt-get install rar unrar p7zip p7zip-rar p7zip-full
#### mtp设备支持
	sudo apt-get install mtpfs libfuse-dev libmad0-dev
##### ubuntu color,D55
#### 安装文字浏览器
	sudo apt-get install w3m
#### [wps](http://community.wps.cn/download/)
#### 安装sublime-text
	sudo add-apt-repository ppa:webupd8team/sublime-text-2
	sudo apt-get update
	sudo apt-get install sublime-text
#### 安装node 
	sudo add-apt-repository ppa:chris-lea/node.js

	sudo apt-get install python-wxtools sysstat

#### 查看爆破ssh
	cat /var/log/secure | awk '/Failed/{print $(NF-3)}' | sort | uniq -c | awk '{print $2" = "$1;}'

#### 截图工具Shutter

#### 程序启动器Synapse

#### Remmina(ftp,rdp,ssh,vnc)

#### remastersys(打包iso)
https://launchpad.net/
https://launchpad.net/~mutse-young/+archive/ubuntu/remastersys
sudo apt-get install remastersys remastersys-gtk
